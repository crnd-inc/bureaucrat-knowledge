import logging
from odoo import http
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request

_logger = logging.getLogger(__name__)


class KnowledgeBase(http.Controller):

    @http.route('/knowledge', auth='public', website=True)
    def knowledge_main_page(self, **kw):
        values = {}
        Categories = request.env['bureaucrat.knowledge.category']
        cats = Categories.search([('parent_id', '=', False)])

        values.update({
            'categories': cats})

        return request.render(
            'bureaucrat_knowledge_website.knowledge_main', values)

    @http.route('/knowledge/<model("bureaucrat.knowledge.category"):categ>',
                auth='public', website=True)
    def knowledge_category(self, categ, **kw):
        values = {}
        Categories = request.env['bureaucrat.knowledge.category']
        cats = Categories.search([('parent_id', '=', categ.id)])
        Documents = request.env['bureaucrat.knowledge.document']
        docs = Documents.search([('category_id', '=', categ.id)])
        parents = self.calc_parents(categ)

        values.update({
            'main_object': categ,
            'categories': cats,
            'documents': docs,
            'parents': parents})

        return request.render(
            'bureaucrat_knowledge_website.knowledge_categories', values)

    @http.route('/knowledge/doc/<model("bureaucrat.knowledge.document"):doc>',
                auth='public', website=True)
    def knowledge_document(self, doc, **kw):
        values = {}
        doc = request.env['bureaucrat.knowledge.document'].browse(doc.id)

        if not doc:
            raise request.not_found()

        parents = self.calc_parents(doc.category_id)
        values.update({
            'doc': doc,
            'main_object': doc,
            'parents': parents})

        return request.render(
            'bureaucrat_knowledge_website.knowledge_document', values)

    @http.route(['/knowledge/search',
                 '/knowledge/search/page/<int:page>',
                 ], auth='public', website=True)
    def knowledge_document_search(self, search="", page=0, **post):
        domain = ['|', ('name', 'ilike', search),
                  ('tag_ids.name', 'ilike', search)]
        documents = request.env['bureaucrat.knowledge.document']
        url = '/knowledge/search'
        keep = QueryURL(url, [], search=search, **post)
        total = documents.search_count(domain)
        pager = request.website.pager(
            url=url, total=total, page=page,
            step=20, url_args=dict(post, search=search))
        docs = request.env['bureaucrat.knowledge.document'].search(
            domain, limit=20, offset=pager['offset'])
        values = {
            'search': search,
            'docs_list': docs,
            'pager': pager,
            'default_url': url,
            'docs_count': total,
            'keep': keep,
        }
        return request.render(
            'bureaucrat_knowledge_website.knowledge_main_with_search_result',
            values)

    def calc_parents(self, parent):
        """ Find list of parents of category,
            when first item list is top-level parent category,
            and last item is original category.
        """
        parents = []
        while parent:
            parents += parent
            parent = parent.parent_id
        parents.reverse()
        return parents
