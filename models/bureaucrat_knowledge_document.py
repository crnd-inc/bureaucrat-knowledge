from urllib.parse import urlencode, quote_plus

from odoo import api, fields, models


class BureaucratKnowledgeDocument(models.Model):
    _name = 'bureaucrat.knowledge.document'
    _inherit = [
        'bureaucrat.knowledge.document',
        'website.seo.metadata',
    ]

    pdf_src_url = fields.Char(compute='_compute_src_url', store=False)

    website_url = fields.Char(
        'Website URL',
        compute='_compute_website_url',
        help='The full URL to access the document through the website.')

    @api.depends('document_type')
    def _compute_src_url(self):
        for record in self:
            if record.document_type == 'pdf':
                query_obj = {
                    'model': 'bureaucrat.knowledge.document',
                    'field': 'document_body_pdf',
                    'id': record.id,
                }
                fileURI = '%s%s' % ('/web/image?', urlencode(
                    query_obj, quote_via=quote_plus))
                viewerURL = '/web/static/lib/pdfjs/web/viewer.html?'
                record.pdf_src_url = viewerURL + urlencode({'file': fileURI})

    @api.depends()
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
