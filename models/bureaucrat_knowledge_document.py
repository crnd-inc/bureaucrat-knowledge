from odoo import models, fields, api


class BureaucratKnowledgeDocument(models.Model):
    _name = 'bureaucrat.knowledge.document'
    _inherit = [
        'generic.tag.mixin',
        'mail.thread',
    ]

    name = fields.Char(translate=True, index=True, required=True)
    document_body = fields.Html(
        compute='_compute_document_body',
        inverse='_inverse_document_body')
    category_id = fields.Many2one(
        'bureaucrat.knowledge.category', index=True, ondelete='restrict')
    history_ids = fields.One2many(
        'bureaucrat.knowledge.document.history', 'document_id')
    commit_summary = fields.Char()

    @api.depends('history_ids', 'history_ids.document_body')
    def _compute_document_body(self):
        for rec in self:
            if rec.history_ids:
                history = rec.history_ids
                rec.document_body = history[0].document_body
            else:
                rec.document_body = False

    # @api.onchange('document_body')
    def _inverse_document_body(self):
        self.env['bureaucrat.knowledge.document.history'].create({
            'commit_summary': self.commit_summary,
            'document_body': self.document_body,
            'user_id': self.env.user.id,
            'date_create': fields.Datetime.now(),
            'document_id': self.id,
        })
