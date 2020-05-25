import datetime
from odoo import models, fields


class BureaucratKnowledgeDocumentHistory(models.Model):
    _name = 'bureaucrat.knowledge.document.history'
    _order = 'date_create DESC'

    commit_summary = fields.Char()
    document_body = fields.Html()
    user_id = fields.Many2one('res.users')
    date_create = fields.Datetime(default=datetime.datetime.now())
    document_id = fields.Many2one('bureaucrat.knowledge.document')
