from odoo import models, fields, api


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
        'bureaucrat.knowledge.document.history', 'document_id')
    latest_history_id = fields.Many2one(
        'bureaucrat.knowledge.document.history',
        compute='_compute_document_latest_history_id',
        readonly=True, store=True, auto_join=True)
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
        store=True, index=True)

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
        compute='_compute_actual_editor_groups_users')
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
        compute='_compute_actual_editor_groups_users')

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
        compute='_compute_actual_owner_groups_users')
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
        compute='_compute_actual_owner_groups_users')

    _sql_constraints = [
        ("check_visibility_type_parent_not_in_the_top_categories",
         "CHECK (category_id IS NOT NULL OR"
         "(category_id IS NULL AND visibility_type != 'parent'))",
         "Document must have a parent category"
         " to set Visibility Type 'Parent'"
         ),
    ]

    def _get_actual_editors_ids(self, rec):
        actual_editor_users_ids = rec.editor_user_ids.ids
        actual_editor_groups_ids = rec.editor_group_ids.ids
        if rec.category_id:
            rec = rec.category_id
            actual_editor_users_ids += rec.editor_user_ids.ids
            actual_editor_groups_ids += rec.editor_group_ids.ids
            parent = rec.parent_id
            while rec.visibility_type == 'parent' and parent:
                rec = parent
                parent = rec.parent_id
                actual_editor_users_ids += rec.editor_user_ids.ids
                actual_editor_groups_ids += rec.editor_group_ids.ids
        return (list(set(actual_editor_users_ids)),
                list(set(actual_editor_groups_ids)))

    def _add_actual_editors(self, rec):
        actual_edit_users, actual_edit_groups = (
            self._get_actual_editors_ids(rec))
        rec.actual_editor_user_ids = actual_edit_users
        rec.actual_editor_group_ids = actual_edit_groups

    def _get_actual_owners_ids(self, rec):
        actual_owner_users_ids = rec.owner_user_ids.ids
        actual_owner_groups_ids = rec.owner_group_ids.ids
        if rec.category_id:
            rec = rec.category_id
            actual_owner_users_ids += rec.owner_user_ids.ids
            actual_owner_groups_ids += rec.owner_group_ids.ids
            parent = rec.parent_id
            while rec.visibility_type == 'parent' and parent:
                rec = parent
                parent = rec.parent_id
                actual_owner_users_ids += rec.owner_user_ids.ids
                actual_owner_groups_ids += rec.owner_group_ids.ids
        return (list(set(actual_owner_users_ids)),
                list(set(actual_owner_groups_ids)))

    def _add_actual_owners(self, rec):
        actual_owner_users, actual_owner_groups = (
            self._get_actual_owners_ids(rec))
        rec.actual_owner_user_ids = actual_owner_users
        rec.actual_owner_group_ids = actual_owner_groups

    @api.depends(
        'visibility_type',
        'category_id',
        'category_id.visibility_type',
        'category_id.parent_ids.parent_id',
        'category_id.parent_ids.visibility_type',
    )
    def _compute_actual_visibility_category_id(self):
        for rec in self:
            parent = rec.category_id
            while parent.visibility_type == 'parent' and parent.parent_id:
                parent = parent.parent_id

            rec.actual_visibility_category_id = parent

    @api.depends(
        'editor_group_ids',
        'editor_user_ids',
        'category_id',
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
            self._add_actual_editors(rec)

    @api.depends(
        'owner_group_ids',
        'owner_user_ids',
        'category_id',
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
            self._add_actual_owners(rec)

    @api.model
    def create(self, vals):
        # TODO: move to defaults level
        if vals.get('category_id', False):
            vals['visibility_type'] = 'parent'
        else:
            vals['visibility_type'] = 'restricted'
            vals['owner_user_ids'] = [(4, self.env.user.id)]

        document = super(BureaucratKnowledgeDocument, self).create(vals)
        self._add_actual_editors(document)
        return document

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
