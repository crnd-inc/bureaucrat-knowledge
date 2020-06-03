from odoo import models, fields, api


class BureaucratKnowledgeDocument(models.Model):
    _name = 'bureaucrat.knowledge.document'
    _description = 'Bureaucrat Knowledge: Document'
    _inherit = [
        'generic.tag.mixin',
        'mail.thread',
        'mail.activity.mixin',
    ]
    _order = 'name, id'

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

    message_notes_ids = fields.One2many(
        'mail.message', 'res_id', string='Discussion Messages', store=False,
        compute="_compute_message_notes_ids", compute_sudo=False)

    @api.depends('message_ids')
    def _compute_message_comments_ids(self):
        for category in self:
            category.message_coments_ids = category.message_ids.filtered(
                lambda r: r.subtype_id == self.env.ref('mail.mt_comment'))


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
