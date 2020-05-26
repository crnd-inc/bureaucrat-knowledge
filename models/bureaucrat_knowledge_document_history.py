import datetime
from odoo import models, fields


class BureaucratKnowledgeDocumentHistory(models.Model):
    _name = 'bureaucrat.knowledge.document.history'
    _order = 'date_create DESC'

    commit_summary = fields.Char()
    document_body = fields.Html()
    user_id = fields.Many2one(
        'res.users',
        index=True, required=True, readony=True,
        default=lambda self: self.env.user.id,
    )
    date_create = fields.Datetime(
        default=datetime.datetime.now(),
        index=True, required=True, readony=True)
    document_id = fields.Many2one(
        'bureaucrat.knowledge.document',
        index=True, required=True, readony=True)
