from odoo import models, fields, api
from odoo.addons.generic_mixin import post_write


class BureaucratKnowledgeCategory(models.Model):
    _name = 'bureaucrat.knowledge.category'
    _description = "Bureaucrat Knowledge: Category"
    _parent_store = True
    _parent_name = 'parent_id'
    _parent_order = 'name'
    _inherit = [
        'generic.tag.mixin',
        'generic.mixin.parent.names',
        'generic.mixin.track.changes',
        'generic.mixin.data.updatable',
        'mail.thread',
    ]
    _order = 'name, id'

    _auto_set_noupdate_on_write = True

    name = fields.Char(translate=True, index=True, required=True)
    description = fields.Html()
    parent_id = fields.Many2one(
        'bureaucrat.knowledge.category', index=True, ondelete='cascade')
    parent_left = fields.Integer('Left Parent', index=True)
    parent_right = fields.Integer('Right Parent', index=True)
    child_ids = fields.One2many(
        'bureaucrat.knowledge.category', 'parent_id')
    child_category_count = fields.Integer(
        compute='_compute_child_category_count')
    document_ids = fields.One2many(
        'bureaucrat.knowledge.document', 'category_id')
    documents_count = fields.Integer(compute='_compute_documents_count')
    active = fields.Boolean(default=True, index=True)

    category_contents = fields.Html(
        compute='_compute_category_contents')

    visibility_type = fields.Selection(
        selection=[
            ('public', 'Public'),
            ('portal', 'Portal'),
            ('internal', 'Internal'),
            ('subscribers', 'Subscribers'),
            ('restricted', 'Restricted'),
            ('parent', 'Parent')],
    )
    parent_visibility_type = fields.Char(
        compute='_compute_parent_visibility_type',
        readonly=True, store=True)

    visibility_group_ids = fields.Many2many(
        comodel_name='res.groups',
        relation='bureaucrat_knowledge_category_visibility_groups',
        column1='knowledge_category_id',
        column2='group_id',
        string='Readers groups')
    visibility_user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='bureaucrat_knowledge_category_visibility_users',
        column1='knowledge_category_id',
        column2='user_id',
        string='Readers')

    editor_group_ids = fields.Many2many(
        comodel_name='res.groups',
        relation='bureaucrat_knowledge_category_editor_groups',
        column1='knowledge_category_id',
        column2='group_id',
        string='Editors groups')
    editor_user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='bureaucrat_knowledge_category_editor_users',
        column1='knowledge_category_id',
        column2='user_id',
        string='Editors')

    owner_group_ids = fields.Many2many(
        comodel_name='res.groups',
        relation='bureaucrat_knowledge_category_owner_groups',
        column1='knowledge_category_id',
        column2='group_id',
        string='Owners groups')
    owner_user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='bureaucrat_knowledge_category_owner_users',
        column1='knowledge_category_id',
        column2='user_id',
        string='Owners')

    @api.model
    def create(self, vals):
        if vals.get('parent_id', False):
            vals['visibility_type'] = 'parent'
        else:
            vals['visibility_type'] = 'subscribers'

        category = super(BureaucratKnowledgeCategory, self).create(vals)
        category.write({'owner_user_ids': [(4, self.env.user.id)]})
        return category

    @api.depends('child_ids')
    def _compute_child_category_count(self):
        for rec in self:
            rec.child_category_count = len(rec.child_ids)

    @api.depends('document_ids')
    def _compute_documents_count(self):
        for rec in self:
            rec.documents_count = len(rec.document_ids)

    @api.depends('child_ids', 'document_ids')
    def _compute_category_contents(self):
        tmpl = self.env.ref(
            'bureaucrat_knowledge.knowledge_category_content_template')
        for rec in self:
            if rec.child_ids or rec.document_ids:
                rec.category_contents = tmpl.render({
                    'category': rec,
                })
            else:
                rec.category_contents = False

    def action_view_subcategories(self):
        self.ensure_one()
        action = self.env.ref(
            'bureaucrat_knowledge.action_bureaucrat_knowledge_category'
        ).read()[0]
        action['domain'] = [('parent_id', '=', self.id)]
        action['context'] = {'default_parent_id': self.id}
        return action

    def action_view_documents(self):
        self.ensure_one()
        action = self.env.ref(
            'bureaucrat_knowledge.action_bureaucrat_knowledge_document'
        ).read()[0]
        action['domain'] = [('category_id', '=', self.id)]
        action['context'] = {'default_category_id': self.id}
        return action

    @post_write('active')
    def _post_active_changed(self, changes):
        for rec in self:
            self.with_context(active_test=False).search(
                [('parent_id', 'child_of', rec.id),
                 ('active', '!=', rec.active)]).write({'active': rec.active})
            self.env['bureaucrat.knowledge.document'].with_context(
                active_test=False).search(
                    [('category_id', 'child_of', rec.id),
                     ('active', '!=', rec.active)]).write(
                         {'active': rec.active})

    def _check_visibility(self, rec):
        if rec.visibility_type == 'parent':
            parent = rec.parent_id
            while rec.visibility_type == 'parent' and parent:
                rec = parent
                parent = rec.parent_id
            return rec.visibility_type

    @post_write('visibility_type')
    def _compute_parent_visibility_type(self, changes):
        for rec in self:
            rec.parent_visibility_type = self._check_visibility(rec)
