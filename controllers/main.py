from odoo import http
from odoo.http import request


class KnowledgeBase(http.Controller):
    @http.route('/knowledge', auth='public', website=True)
    def knowledge_main(self, **kw):
        return http.request.render(
            'bureaucrat_knowledge_website.knowledge_main', {})

    @http.route('/knowledge/categories', auth='public', website=True)
    def knowledge_categories(self, **kw):
        Categories = request.env['bureaucrat.knowledge.category']
        cats = Categories.search([])
        return http.request.render(
            'bureaucrat_knowledge_website.knowledge_categories', {
                'categories': cats})

    @http.route('/knowledge/documents', auth='public', website=True)
    def knowledge_documents(self, **kw):
        Documents = request.env['bureaucrat.knowledge.document']
        docs = Documents.search([])
        return http.request.render(
            'bureaucrat_knowledge_website.knowledge_documents', {
                'documents': docs})
