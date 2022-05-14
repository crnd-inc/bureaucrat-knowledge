from odoo import models, fields


class RequestsWizardManageRelatedDocuments(models.TransientModel):
    _name = "document.wizard.manage.related.documents"
    _description = 'Documents Wizard: Manage related documents'

    def _get_related_document_ids_domain(self):
        return [('id', '!=', self.env.context.get('default_document_id'))]

    def _get_default_related_document_ids(self):
        document_obj = self.env['bureaucrat.knowledge.document']
        default_document_id = self.env.context.get('default_document_id')
        return document_obj.browse(default_document_id).related_document_ids

    document_id = fields.Many2one('bureaucrat.knowledge.document', 'Document')
    related_document_ids = fields.Many2many(
        'bureaucrat.knowledge.document',
        relation='bkd_document_document_rel',
        domain=_get_related_document_ids_domain,
        default=_get_default_related_document_ids,
        string='Related documents')

    def action_change_related_documents(self):
        for rec in self:
            rec.document_id.related_document_ids = rec.related_document_ids
