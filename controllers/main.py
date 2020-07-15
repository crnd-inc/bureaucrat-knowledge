import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class KnowledgeBase(http.Controller):

    @http.route(['/knowledge',
                 '/knowledge/<model("bureaucrat.knowledge.category"):categ>'],
                auth='public', website=True)
    def knowledge_category(self, categ=False, **kw):
        values = {}
        Categories = request.env['bureaucrat.knowledge.category']
        cat_id = False
        if categ:
            cat_id = categ.id
        cats = Categories.search([('parent_id', '=', cat_id)])
        Documents = request.env['bureaucrat.knowledge.document']
        docs = Documents.search([('category_id', '=', cat_id)])

        parents = self.calc_parents(categ)

        values.update({
            'categories': cats,
            'documents': docs,
            'parents': parents})

        return request.render(
            'bureaucrat_knowledge_website.knowledge_main', values)

    @http.route('/knowledge/doc/<model("bureaucrat.knowledge.document"):doc>',
                auth='public', website=True)
    def knowledge_document(self, doc, **kw):
        values = {}
        doc = request.env['bureaucrat.knowledge.document'].browse(doc.id)

        if not doc:
            raise request.not_found()

        parents = self.calc_parents(doc)
        values.update({
            'doc': doc,
            'parents': parents})

        return request.render(
            'bureaucrat_knowledge_website.knowledge_document', values)

    def calc_parents(self, parent):
        if parent and parent._name == 'bureaucrat.knowledge.document':
            parent = parent.category_id
        parents = []
        while parent:
            parents += parent
            parent = parent.parent_id
        parents.reverse()
        return parents
