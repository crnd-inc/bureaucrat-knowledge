from .common import TestTourKnowledge


class TestSearch(TestTourKnowledge):

    def setUp(self):
        super(TestSearch, self).setUp()
        self.user_demo = self.env.ref(
            'bureaucrat_knowledge_website.user_demo_service_desk_website')
        self.group_portal = self.env.ref('base.group_portal')

    def test_tour(self):
        self._test_phantom_tour(
            '/', 'bureaucrat_knowledge_website_search',
            login=self.user_demo.login)
