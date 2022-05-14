from odoo.tests.common import tagged
from .common import TestPhantomTour


@tagged('post_install', '-at_install')
class TestSearch(TestPhantomTour):
    def setUp(self):
        super(TestSearch, self).setUp()
        self.manager = self.env.ref(
            'bureaucrat_knowledge_website.user_demo_knowledge_website_manager')

    def test_tour_knowledge_web(self):
        self._test_phantom_tour(
            '/', 'bureaucrat_knowledge_website_search',
            login=self.manager.login)
