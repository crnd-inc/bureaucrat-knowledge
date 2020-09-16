from odoo.tests.common import SavepointCase
from odoo.addons.generic_mixin.tests.common import (
    ReduceLoggingMixin,
    AccessRulesFixMixinST,
)


class TestBureaucratKnowledgeBase(ReduceLoggingMixin,
                                  AccessRulesFixMixinST,
                                  SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestBureaucratKnowledgeBase, cls).setUpClass()

        # User
        cls.user = cls.env.ref('base.user_demo')
        cls.portal_user = cls.env.ref('base.demo_user0')
        cls.public_user = cls.env.ref('base.public_user')

        # Groups
        cls.group_knowledge_user_implicit = cls.env.ref(
            'bureaucrat_knowledge.group_bureaucratic_knowledge_user_implicit')
        cls.group_knowledge_user = cls.env.ref(
            'bureaucrat_knowledge.group_bureaucratic_knowledge_user')
        cls.group_knowledge_manager = cls.env.ref(
            'bureaucrat_knowledge.group_bureaucratic_knowledge_manager')
        cls.group_employee = cls.env.ref('base.group_user')

        # Test categories
        cls.category_top_level = cls.env.ref(
            'bureaucrat_knowledge.bureaucrat_demo_top_level_1')
        cls.category_subcat_1 = cls.env.ref(
            'bureaucrat_knowledge.bureaucrat_demo_subcategory_1')
        cls.category_subcat_2 = cls.env.ref(
            'bureaucrat_knowledge.bureaucrat_demo_subcategory_2')
        cls.document_demo_top_1 = cls.env.ref(
            'bureaucrat_knowledge.document_demo_top_1')
        cls.document_subcat_2 = cls.env.ref(
            'bureaucrat_knowledge.document_demo_sub_2')
