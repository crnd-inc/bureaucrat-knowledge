from odoo import models, fields

DOC_TYPE = [
    ('html', 'html'),
    ('pdf', 'pdf'),
]


class BureaucratKnowledgeDocumentHistory(models.Model):
    _name = 'bureaucrat.knowledge.document.history'
    _description = 'Bureaucrat Knowledge: Document History'
    _order = 'date_create DESC'

    _auto_set_noupdate_on_write = True

    commit_summary = fields.Char()
    document_type = fields.Selection(
        selection=DOC_TYPE, required=True)
    document_body = fields.Html()
    document_body_pdf = fields.Binary()
    user_id = fields.Many2one(
        'res.users',
        index=True, required=True, readonly=True,
        default=lambda self: self.env.user.id,
    )
    date_create = fields.Datetime(
        default=fields.Datetime.now,
        index=True, required=True, readonly=True)
    document_id = fields.Many2one(
        'bureaucrat.knowledge.document',
        ondelete='cascade', index=True, required=True, readonly=True)
