from odoo import models, fields


class BureaucratKnowledgeDocument(models.Model):
    _name = 'bureaucrat.knowledge.document'
    _inherit = [
        'generic.tag.mixin',
        'mail.thread',
    ]

    name = fields.Char(translate=True, index=True, required=True)
    document_body = fields.Html()
    category_id = fields.Many2one(
        'bureaucrat.knowledge.category', index=True, ondelete='restrict')
