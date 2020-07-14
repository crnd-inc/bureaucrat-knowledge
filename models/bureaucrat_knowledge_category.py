from odoo import models


class BureaucratKnowledgeCategory(models.Model):
    _name = 'bureaucrat.knowledge.category'
    _inherit = [
        'bureaucrat.knowledge.category',
        'website.seo.metadata',
        'portal.mixin',
    ]

    def _compute_portal_url(self):
        res = super(BureaucratKnowledgeCategory, self)._compute_portal_url()
        for category in self:
            category.portal_url = '/knowledge/%s' % category.id
        return res

    def action_show_on_website(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.portal_url,
            'target': 'self',
        }
