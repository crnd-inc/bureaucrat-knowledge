from odoo import http
from odoo.http import request


class KnowledgeBase(http.Controller):
    @http.route('/knowledge', auth='public', website=True)
    def knowledge_main(self, **kw):
        return request.render(
            'bureaucrat_knowledge_website.knowledge_main', {})

    @http.route('/knowledge/categories', auth='public', website=True)
    def knowledge_categories(self, **kw):
        Categories = request.env['bureaucrat.knowledge.category']
        cats = Categories.search([])
        return request.render(
            'bureaucrat_knowledge_website.knowledge_categories', {
                'categories': cats})

    @http.route('/knowledge/documents', auth='public', website=True)
    def knowledge_documents(self, **kw):
        Documents = request.env['bureaucrat.knowledge.document']
        docs = Documents.search([])
        return request.render(
            'bureaucrat_knowledge_website.knowledge_documents', {
                'documents': docs})

    @http.route('/knowledge/documents/<int:doc_id>',
                auth='public', website=True)
    def document(self, doc_id, **kw):
        values = {}
        docs = request.env['bureaucrat.knowledge.document'].search(
            [('id', '=', doc_id)])

        if not docs:
            raise request.not_found()

        values.update({'doc': docs})

        return request.render(
            'bureaucrat_knowledge_website.knowledge_document', values)
