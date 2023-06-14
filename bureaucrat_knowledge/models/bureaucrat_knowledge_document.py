import io
import logging
import base64
import PyPDF2
from lxml import html  # nosec

import pdf2image

from odoo import models, fields, api
from odoo.addons.generic_mixin import pre_write, post_write
from ..tools.utils import _get_preview_from_html

_logger = logging.getLogger(__name__)

DOC_TYPE = [
    ('html', 'html'),
    ('pdf', 'pdf'),
]


class BureaucratKnowledgeDocument(models.Model):
    _name = 'bureaucrat.knowledge.document'
    _description = 'Bureaucrat Knowledge: Document'
    _inherit = [
        'generic.tag.mixin',
        'generic.mixin.track.changes',
        'generic.mixin.data.updatable',
        'generic.mixin.get.action',
        'mail.thread',
        'mail.activity.mixin',
    ]
    _order = 'sequence, code, name, id'

    _auto_set_noupdate_on_write = True

    @api.model
    def default_get(self, default_fields):
        res = super(BureaucratKnowledgeDocument, self).default_get(
            default_fields)
        type_article = self.env.ref(
            'bureaucrat_knowledge.bureaucrat_document_type_art')
        res['document_type_id'] = type_article.id
        return res

    name = fields.Char(translate=True, index=True, required=True)
    document_number = fields.Char(index=True, required=False, size=5)
    code = fields.Char(
        compute='_compute_code', store=True, index=True, readonly=True)
    document_format = fields.Selection(
        default='html',
        selection=DOC_TYPE,
        required=True,
    )
    document_type = fields.Selection(
        selection=DOC_TYPE,
        readonly=True,
        compute='_compute_document_type',
        inverse='_inverse_document_type',
    )
    document_body_html = fields.Html()
    document_body_pdf = fields.Binary(attachment=True)
    document_preview_text = fields.Text(
        compute='_compute_preview',
        store=True)
    document_preview_image = fields.Binary(
        "Preview",
        attachment=True,
        compute='_compute_preview',
        store=True)
    category_id = fields.Many2one(
        'bureaucrat.knowledge.category', index=True, ondelete='restrict')
    category_full_name = fields.Char(related='category_id.full_name')
    history_ids = fields.One2many(
        'bureaucrat.knowledge.document.history', 'document_id', auto_join=True)
    history_count = fields.Integer(
        compute='_compute_document_history', compute_sudo=True,
        store=True, readonly=True)
    latest_history_id = fields.Many2one(
        'bureaucrat.knowledge.document.history',
        compute='_compute_document_history',
        readonly=True, store=True, auto_join=True, compute_sudo=True)
    commit_summary = fields.Char(store=True)
    index_document_body = fields.Text(
        store=True, compute='_compute_index_body')
    document_type_id = fields.Many2one(
        'bureaucrat.document.type', index=True,
        required=True, ondelete='restrict',
        auto_join=True)

    active = fields.Boolean(default=True, index=True)
    color = fields.Integer('Color Index', readonly=False)

    created_by_id = fields.Many2one(
        'res.users', 'Created by',
        readonly=True, ondelete='restrict', index=True,
        help="Document was created by this user", copy=False)

    visibility_type = fields.Selection(
        selection=[
            ('public', 'Public'),
            ('portal', 'Portal'),
            ('internal', 'Internal'),
            ('restricted', 'Restricted'),
            ('parent', 'Parent')],
    )

    actual_visibility_category_id = fields.Many2one(
        'bureaucrat.knowledge.category',
        compute='_compute_actual_visibility_category_id',
        store=True, index=True, compute_sudo=True)

    # Readers
    visibility_group_ids = fields.Many2many(
        comodel_name='res.groups',
        relation='bureaucrat_knowledge_document_visibility_groups',
        column1='knowledge_document_id',
        column2='group_id',
        string='Readers groups')
    visibility_user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='bureaucrat_knowledge_document_visibility_users',
        column1='knowledgey_document_id',
        column2='user_id',
        string='Readers')

    # Editors
    editor_group_ids = fields.Many2many(
        comodel_name='res.groups',
        relation='bureaucrat_knowledge_document_editor_groups',
        column1='knowledge_document_id',
        column2='group_id',
        string='Editors groups')
    actual_editor_group_ids = fields.Many2many(
        comodel_name='res.groups',
        relation='bureaucrat_knowledge_document_actual_editor_groups',
        column1='knowledge_document_id',
        column2='group_id',
        string='Actual editors groups',
        readonly=True,
        store=True,
        compute='_compute_actual_editor_groups_users',
        compute_sudo=True)
    editor_user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='bureaucrat_knowledge_document_editor_users',
        column1='knowledge_document_id',
        column2='user_id',
        string='Editors')
    actual_editor_user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='bureaucrat_knowledge_document_actual_editor_users',
        column1='knowledge_document_id',
        column2='user_id',
        string='Actual editors',
        readonly=True,
        store=True,
        compute='_compute_actual_editor_groups_users',
        compute_sudo=True)

    # Owners
    owner_group_ids = fields.Many2many(
        comodel_name='res.groups',
        relation='bureaucrat_knowledge_document_owner_groups',
        column1='knowledge_document_id',
        column2='group_id',
        string='Owners groups')
    actual_owner_group_ids = fields.Many2many(
        comodel_name='res.groups',
        relation='bureaucrat_knowledge_document_actual_owner_groups',
        column1='knowledge_document_id',
        column2='group_id',
        string='Actual owners groups',
        readonly=True,
        store=True,
        compute='_compute_actual_owner_groups_users',
        compute_sudo=True)
    owner_user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='bureaucrat_knowledge_document_owner_users',
        column1='knowledge__documentid',
        column2='user_id',
        string='Owners')
    actual_owner_user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='bureaucrat_knowledge_document_actual_owner_users',
        column1='knowledge_document_id',
        column2='user_id',
        string='Actual owners',
        readonly=True,
        store=True,
        compute='_compute_actual_owner_groups_users',
        compute_sudo=True)
    sequence = fields.Integer(default=1000, index=True)

    _sql_constraints = [
        ("check_visibility_type_parent_not_in_the_top_categories",
         "CHECK (category_id IS NOT NULL OR"
         "(category_id IS NULL AND visibility_type != 'parent'))",
         "Document must have a parent category "
         "to set Visibility Type 'Parent'"),
        ('document_number_ascii_only',
         r"CHECK (document_number ~ '^[a-zA-Z0-9\-_]*$')",
         'document number must be ascii only'),
    ]

    @api.depends('category_id.code',
                 'document_type_id.code',
                 'document_number')
    def _compute_code(self):
        for rec in self:
            if rec.category_id:
                rec.code = '%s_%s_%s' % (rec.category_id.code,
                                         rec.document_type_id.code,
                                         rec.document_number)
            else:
                rec.code = '%s_%s' % (rec.document_type_id.code,
                                      rec.document_number, )

    @api.depends('document_body_html', 'document_body_pdf', 'document_type')
    def _compute_preview(self):
        for rec in self:
            if rec.document_format == 'pdf':
                rec.document_preview_image = \
                    rec._get_preview_from_pdf()
            if rec.document_format == 'html':
                rec.document_preview_text = \
                    _get_preview_from_html(rec.document_body_html)

    @api.depends(
        'visibility_type',
        'category_id',
        'category_id.parent_id',
        'category_id.visibility_type',
        'category_id.parent_ids.parent_id',
        'category_id.parent_ids.visibility_type',
    )
    def _compute_actual_visibility_category_id(self):
        for rec in self:
            parent = rec.category_id.sudo()
            while parent.visibility_type == 'parent' and parent.parent_id:
                parent = parent.parent_id
            rec.actual_visibility_category_id = parent

    @api.depends(
        'editor_group_ids',
        'editor_user_ids',
        'category_id',
        'category_id.parent_id',
        'category_id.editor_group_ids',
        'category_id.editor_user_ids',
        'category_id.parent_ids.editor_group_ids',
        'category_id.parent_ids.editor_user_ids',
        'category_id.parent_ids.parent_id',
        'category_id.parent_ids.parent_id.editor_group_ids',
        'category_id.parent_ids.parent_id.editor_user_ids',
    )
    def _compute_actual_editor_groups_users(self):
        for rec in self:
            actual_editor_users = rec.editor_user_ids
            actual_editor_groups = rec.editor_group_ids
            if rec.category_id:
                actual_editor_users += rec.category_id.actual_editor_user_ids
                actual_editor_groups += rec.category_id.actual_editor_group_ids
            rec.actual_editor_user_ids = actual_editor_users
            rec.actual_editor_group_ids = actual_editor_groups

    @api.depends(
        'owner_group_ids',
        'owner_user_ids',
        'category_id',
        'category_id.parent_id',
        'category_id.owner_group_ids',
        'category_id.owner_user_ids',
        'category_id.parent_ids.owner_group_ids',
        'category_id.parent_ids.owner_user_ids',
        'category_id.parent_ids.parent_id',
        'category_id.parent_ids.parent_id.owner_group_ids',
        'category_id.parent_ids.parent_id.owner_user_ids',
    )
    def _compute_actual_owner_groups_users(self):
        for rec in self:
            actual_owner_users = rec.owner_user_ids
            actual_owner_groups = rec.owner_group_ids
            if rec.category_id:
                actual_owner_users += rec.category_id.actual_owner_user_ids
                actual_owner_groups += rec.category_id.actual_owner_group_ids
            rec.actual_owner_user_ids = actual_owner_users
            rec.actual_owner_group_ids = actual_owner_groups

    @api.depends('history_ids')
    def _compute_document_history(self):
        for record in self:
            if record.history_ids:
                record.latest_history_id = record.history_ids.sorted()[0]
            else:
                record.latest_history_id = self.env[
                    'bureaucrat.knowledge.document.history'].browse()
            record.history_count = len(record.history_ids)

    def action_view_history(self):
        self.ensure_one()
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'bureaucrat_knowledge'
            '.action_bureaucrat_knowledge_document_history',
            context={'default_document_id': self.id},
            domain=[
                ('document_id', '=', self.id)
            ],
        )

    def _get_document_index_pdf(self):
        """ Index PDF documents
        """
        # TODO: Maybe there is a better way to do pdf indexing
        self.ensure_one()
        if not self.document_body_pdf:
            return ''

        # TODO: try to compute path to attachment file,
        #       instead of computing base64 content of files
        #       this way, possibly, we could optimize performance
        #       for large PDF files
        try:
            bin_data = base64.b64decode(self.document_body_pdf)
        except Exception:
            _logger.warning('Error in decode data for pdf')

        if not bin_data.startswith(b'%PDF-'):
            return ''

        f = io.BytesIO(bin_data)
        buf = ''
        try:
            pdf = PyPDF2.PdfFileReader(f, overwriteWarnings=False)
            for page in pdf.pages:
                buf += page.extractText()
        except Exception:
            _logger.warning('Error in get index data for pdf')
        return buf

    def _get_document_index_html(self):
        """ parse html content and remove all tags, keeping only words
            to be searched
        """
        self.ensure_one()
        if not self.document_body_html:
            return ''
        try:
            index_content = html.document_fromstring(
                self.document_body_html
            ).text_content()
        except (ValueError, TypeError):
            return ''
        return index_content

    def _get_document_index(self):
        """ Compute index content for the document.
            Could be used for searches
        """
        if self.document_format == 'html':
            return self._get_document_index_html()
        if self.document_format == 'pdf':
            return self._get_document_index_pdf()
        return ''

    def _get_preview_from_pdf(self):
        self.ensure_one()
        if not self.document_body_pdf:
            return ''

        try:
            pdf_content = base64.b64decode(self.document_body_pdf)

            # TODO: This could take a lot of memory on large PDF,
            #       thus we have to think how to optimize this.
            preview = pdf2image.convert_from_bytes(pdf_content)
        except Exception:
            _logger.error('Error in decode data for pdf', exc_info=True)
            # Cannot generate preview image, this we have return empty string
            # to show no preview, but do not fail with error.
            # Absence of preview is not critical, thus there is no sense
            # to raise error here.
            return ''

        byte_io = io.BytesIO()
        preview[0].save(byte_io, 'PNG')
        return base64.b64encode(byte_io.getvalue())

    @api.depends('document_format', 'document_body_html', 'document_body_pdf')
    def _compute_index_body(self):
        for rec in self:
            rec.index_document_body = rec._get_document_index()

    @api.onchange('category_id', 'visibility_type')
    def _onchange_categ_visibility_type(self):
        for record in self:
            if record.category_id and not record.visibility_type:
                record.visibility_type = 'parent'
            elif record.visibility_type == 'parent' and not record.category_id:
                record.visibility_type = False

    def _save_document_history(self):
        history_data = []
        for document in self:
            history_vals = {
                'document_id': document.id,
                'document_name': document.name,
                'commit_summary': document.commit_summary,
                'document_format': document.document_format,
            }

            # TODO: move preparing data logic to separate method,
            #       to simplify further extension of knowledge base
            #       with new document types
            if document.document_format == 'html':
                history_vals.update({
                    'document_body_html': document.document_body_html,
                })
            elif document.document_format == 'pdf':
                history_vals.update({
                    'document_body_pdf': document.document_body_pdf,
                })

            history_data += [history_vals]

        self.env['bureaucrat.knowledge.document.history'].create(history_data)
        self.write({'commit_summary': False})

    @api.model_create_multi
    def create(self, vals):
        self.check_access_rights('create')

        values = []
        for v in vals:
            v = dict(v)
            # TODO: move to defaults level
            if v.get('category_id', False):
                v['visibility_type'] = 'parent'
            else:
                v['visibility_type'] = 'restricted'
                v['owner_user_ids'] = [(4, self.env.user.id)]

            # This is required to display the author of the document correctly
            v.update({'created_by_id': self.env.user.id})

            values += [v]

        documents = super(BureaucratKnowledgeDocument, self.sudo()).create(
            values)
        # reference created document as self.env (because before this document
        # is referenced as sudo)
        documents = documents.with_env(self.env)

        # Enforce check of access rights after document created,
        # to ensure that current user has access to create this document
        documents.check_access_rule('create')
        documents._save_document_history()
        return documents

    @pre_write('document_format')
    def _before_document_changed(self, changes):
        old_doc_type, __ = changes['document_format']
        if old_doc_type == 'html':
            return {'document_body_html': False}
        if old_doc_type == 'pdf':
            return {'document_body_pdf': False}
        return False

    @post_write(
        'name',
        'document_format',
        'document_body_html',
        'document_body_pdf')
    def _post_document_changed(self, changes):
        self._save_document_history()

    @api.depends('document_format')
    def _compute_document_type(self):
        for rec in self:
            rec.document_type = rec.document_format

    @api.multi
    def _inverse_document_type(self):
        for rec in self:
            rec.document_format = rec.document_type
            _logger.warning(
                "Field 'document_type' on bureaucrat.knowledge.document "
                "is deprecated and should be removed.")

    @api.model
    def _add_missing_default_values(self, values):
        res = super(
            BureaucratKnowledgeDocument, self
        )._add_missing_default_values(values)

        new_doc = self.new(res)
        if not new_doc.document_number and new_doc.document_type_id:
            res['document_number'] = (
                new_doc.document_type_id.sudo().
                number_generator_id.next_by_id())
        return res
