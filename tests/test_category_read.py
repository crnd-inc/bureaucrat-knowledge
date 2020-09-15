from odoo.exceptions import AccessError
from .test_common import TestBureaucratKnowledgeBase


class TesteKnowledgeCategoryRead(TestBureaucratKnowledgeBase):

    def test_category_access_read_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

