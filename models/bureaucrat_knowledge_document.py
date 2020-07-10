from odoo import models


class BureaucratKnowledgeDocument(models.Model):
    _name = 'bureaucrat.knowledge.document'
    _inherit = [
        'bureaucrat.knowledge.document',
        'portal.mixin',
    ]

    def _compute_portal_url(self):
        res = super(BureaucratKnowledgeDocument, self)._compute_portal_url()
        for document in self:
            document.portal_url = '/knowledge/doc/%s' % document.id
        return res

    def action_show_on_website(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.portal_url,
            'target': 'self',
        }
