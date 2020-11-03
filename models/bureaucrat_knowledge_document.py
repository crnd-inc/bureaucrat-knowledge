import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class BureaucratKnowledgeDocument(models.Model):
    _name = 'bureaucrat.knowledge.document'
    _description = 'Bureaucrat Knowledge: Document'
    _inherit = [
        'generic.tag.mixin',
        'generic.mixin.track.changes',
        'generic.mixin.data.updatable',
        'mail.thread',
    ]
    _order = 'name, id'

    _auto_set_noupdate_on_write = True

    name = fields.Char(translate=True, index=True, required=True)
    document_body = fields.Html(
        compute='_compute_document_body',
        inverse='_inverse_document_body',
        search='_search_document_body')
    category_id = fields.Many2one(
        'bureaucrat.knowledge.category', index=True, ondelete='restrict')
    history_ids = fields.One2many(
        'bureaucrat.knowledge.document.history', 'document_id', auto_join=True)
    latest_history_id = fields.Many2one(
        'bureaucrat.knowledge.document.history',
        compute='_compute_document_latest_history_id',
        readonly=True, store=True, auto_join=True, compute_sudo=True)
    commit_summary = fields.Char(store=False)
    active = fields.Boolean(default=True, index=True)

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

    _sql_constraints = [
        ("check_visibility_type_parent_not_in_the_top_categories",
         "CHECK (category_id IS NOT NULL OR"
         "(category_id IS NULL AND visibility_type != 'parent'))",
         "Document must have a parent category "
         "to set Visibility Type 'Parent'"),
    ]

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
    def _compute_document_latest_history_id(self):
        for record in self:
            if record.history_ids:
                record.latest_history_id = record.history_ids.sorted()[0]
            else:
                record.latest_history_id = self.env[
                    'bureaucrat.knowledge.document.history'].browse()

    @api.depends('latest_history_id', 'latest_history_id.document_body')
    def _compute_document_body(self):
        for record in self:
            record.document_body = record.latest_history_id.document_body

    def _inverse_document_body(self):
        for record in self:
            if record.document_body == record.latest_history_id.document_body:
                # There is no sense to create new hisstory record if there is
                # no changes (document body is same as in prev record)
                continue

            self.env['bureaucrat.knowledge.document.history'].create({
                'commit_summary': record.commit_summary,
                'document_body': record.document_body,
                'user_id': self.env.user.id,
                'date_create': fields.Datetime.now(),
                'document_id': record.id,
            })

    def _search_document_body(self, operator, value):
        return [('latest_history_id.document_body', operator, value)]

    @api.onchange('category_id', 'visibility_type')
    def _onchange_categ_visibility_type(self):
        for record in self:
            if record.category_id and not record.visibility_type:
                record.visibility_type = 'parent'
            elif record.visibility_type == 'parent' and not record.category_id:
                record.visibility_type = False

    @api.model
    def create(self, vals):
        self.check_access_rights('create')

        # TODO: move to defaults level
        if vals.get('category_id', False):
            vals['visibility_type'] = 'parent'
        else:
            vals['visibility_type'] = 'restricted'
            vals['owner_user_ids'] = [(4, self.env.user.id)]

        document = super(BureaucratKnowledgeDocument, self.sudo()).create(vals)

        # reference created document as self.env (because before this document
        # is referenced as sudo)
        document = document.with_env(self.env)

        # Enforce check of access rights after document created,
        # to ensure that current user has access to create this document
        document.check_access_rule('create')

        return document
