from odoo import models


class BureaucratKnowledgeDocument(models.Model):
    _name = 'bureaucrat.knowledge.document'
    _inherit = [
        'bureaucrat.knowledge.document',
        'website.published.mixin',
        'website.seo.metadata',
    ]

    def _compute_website_url(self):
        res = super(BureaucratKnowledgeDocument, self)._compute_website_url()
        for document in self:
            document.website_url = '/knowledge/doc/%s' % document.id
        return res

    def action_show_on_website(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.website_url,
            'target': 'self',
        }
