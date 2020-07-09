import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class KnowledgeBase(http.Controller):

    @http.route(['/knowledge',
                 '/knowledge/<int:cat_id>',
                 '/knowledge/<int:cat_id>/<int:subcat_id>'],
                auth='public', website=True)
    def knowledge_category(self, cat_id=False, subcat_id=0, **kw):
        Categories = request.env['bureaucrat.knowledge.category']
        if subcat_id:
            cat_id = subcat_id
        cats = Categories.search([('parent_id', '=', cat_id)])
        Documents = request.env['bureaucrat.knowledge.document']
        docs = Documents.search([('category_id', '=', cat_id)])
        _logger.warning("Docs : %s", (cats, docs))
        return request.render(
            'bureaucrat_knowledge_website.knowledge_main', {
                'categories': cats,
                'documents': docs})

    @http.route(['/knowledge/<int:cat_id>/doc/<int:doc_id>',
                 '/knowledge/<int:cat_id>/<int:subcat_id>/doc/<int:doc_id>'],
                auth='public', website=True)
    def document(self, doc_id, cat_id=False, subcat_id=False, **kw):
        values = {}
        docs = request.env['bureaucrat.knowledge.document'].search(
            [('id', '=', doc_id)])

        if not docs:
            raise request.not_found()

        values.update({'doc': docs})

        return request.render(
            'bureaucrat_knowledge_website.knowledge_document', values)
