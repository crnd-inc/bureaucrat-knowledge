from odoo import models, fields, api


class BureaucratKnowledgeDocument(models.Model):
    _inherit = 'bureaucrat.knowledge.document'

    related_document_ids = fields.Many2many(
        'bureaucrat.knowledge.document',
        'document_document_rel', 'related_id', 'related_to_id',
        string='Related Documents',
        help="Other documents referenced from this document")
    related_reverse_document_ids = fields.Many2many(
        'bureaucrat.knowledge.document',
        'document_document_rel', 'related_to_id', 'related_id',
        string='Related to documents',
        help="Documents that have references to this document")
    related_document_count = fields.Integer(
        compute="_compute_related_documents")
    related_reverse_document_count = fields.Integer(
        compute="_compute_related_documents")
    related_document_total_count = fields.Integer(
        compute="_compute_related_documents")

    @api.depends('related_document_ids', 'related_reverse_document_ids')
    def _compute_related_documents(self):
        for doc in self:
            doc.related_document_count = len(doc.related_document_ids)
            doc.related_reverse_document_count = len(
                doc.related_reverse_document_ids)
            doc.related_document_total_count = len(set(
                doc.related_document_ids +
                doc.related_reverse_document_ids))

    def action_view_related_documents(self):
        self.ensure_one()
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'bureaucrat_knowledge.action_bureaucrat_knowledge_document',
            domain=[
                '|',
                ('related_document_ids', '=', self.id),
                ('related_reverse_document_ids', '=', self.id),
            ],
        )

    def action_related_document_manage(self):
        self.ensure_one()
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'bureaucrat_knowledge_rel_docs'
            '.document_wizard_manage_related_documents_action',
            context={'default_document_id': self.id},
        )
