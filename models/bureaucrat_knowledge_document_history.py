import datetime
from odoo import models, fields


class BureaucratKnowledgeDocumentHistory(models.Model):
    _name = 'bureaucrat.knowledge.document.history'
    _description = 'Bureaucrat Knowledge: Document History'
    _order = 'date_create DESC'

    _auto_set_noupdate_on_write = True

    commit_summary = fields.Char()
    document_body = fields.Html()
    user_id = fields.Many2one(
        'res.users',
        index=True, required=True, readonly=True,
        default=lambda self: self.env.user.id,
    )
    date_create = fields.Datetime(
        default=datetime.datetime.now(),
        index=True, required=True, readonly=True)
    document_id = fields.Many2one(
        'bureaucrat.knowledge.document',
        ondelete='cascade', index=True, required=True, readonly=True)
