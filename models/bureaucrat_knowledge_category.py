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
        'mail.thread',
    ]
    _order = 'name'

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

    category_subcategories = fields.Html(
        compute='_compute_category_subcategories')
    category_documents = fields.Html(compute='_compute_category_documents')

    @api.depends('child_ids')
    def _compute_child_category_count(self):
        for rec in self:
            rec.child_category_count = len(rec.child_ids)

    @api.depends('document_ids')
    def _compute_documents_count(self):
        for rec in self:
            rec.documents_count = len(rec.document_ids)

    @api.depends('child_ids')
    def _compute_category_subcategories(self):
        for rec in self:
            html_string = '<ul class="list-group">'
            for cat in rec.child_ids:
                html_string += (
                    '<li class="list-group-item">'
                    '<a href="/web#id=%s&view_type=form&'
                    'model=bureaucrat.knowledge.category&'
                    'action=%s">'
                    '<span class="fa fa-folder mr8"/>%s</a>'
                    '</li>') % (
                        cat.id,
                        self.env.ref(
                            'bureaucrat_knowledge.'
                            'action_bureaucrat_knowledge_category').id,
                        cat.name)
            html_string += '</ul>'
            rec.category_subcategories = html_string

    @api.depends('document_ids')
    def _compute_category_documents(self):
        for rec in self:
            html_string = '<ul class="list-group">'
            for doc in rec.document_ids:
                html_string += (
                    '<li class="list-group-item">'
                    '<a href="/web#id=%s&view_type=form&'
                    'model=bureaucrat.knowledge.document&'
                    'action=%s">'
                    '<span class="fa fa-file mr8"/>%s</a>'
                    '</li>') % (
                        doc.id,
                        self.env.ref(
                            'bureaucrat_knowledge.'
                            'action_bureaucrat_knowledge_document').id,
                        doc.name)
            html_string += '</ul>'
            rec.category_documents = html_string

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
