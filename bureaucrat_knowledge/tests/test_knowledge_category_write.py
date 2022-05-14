from odoo.exceptions import AccessError
from .test_common import TestBureaucratKnowledgeBase


class TestKnowledgeCategoryWrite(TestBureaucratKnowledgeBase):

    @classmethod
    def setUpClass(cls):
        super(TestKnowledgeCategoryWrite, cls).setUpClass()
        cls.demo_user.groups_id |= cls.group_knowledge_user

    # Testing Top level category for visibility_type = 'restricted'
    def test_category_restricted_access_write_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

    def test_category_restricted_access_write_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

    def test_category_restricted_editors_access_write_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.editor_user_ids), 1)
        self.category_top_level.with_user(self.demo_user).write({
            'name': 'Top level category 1 renamed'})

    def test_category_restricted_editors_access_write_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.editor_group_ids), 1)
        self.category_top_level.with_user(self.demo_user).write({
            'name': 'Top level category 1 renamed'})

    def test_category_restricted_owners_access_write_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.owner_group_ids)
        self.assertEqual(len(self.category_top_level.owner_user_ids), 0)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.owner_user_ids), 1)
        self.category_top_level.with_user(self.demo_user).write({
            'name': 'Top level category 1 renamed'})

    def test_category_restricted_owners_access_write_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.owner_group_ids)
        self.assertEqual(len(self.category_top_level.owner_user_ids), 0)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.owner_group_ids), 1)
        self.category_top_level.with_user(self.demo_user).write({
            'name': 'Top level category 1 renamed'})

    # Testing Top level category for visibility_type = 'public'
    def test_category_public_access_write_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.public_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.public_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.public_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'public'

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.public_user).write({
                'name': 'Top level category 1 renamed'})

    # Testing Top level category for visibility_type = 'portal'
    def test_category_portal_access_write_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.portal_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.portal_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.portal_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.portal_user).write({
                'name': 'Top level category 1 renamed'})

    # Testing Top level category for visibility_type = 'internal'
    def test_category_internal_access_write_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'internal'

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

    # Testing subcategory 2nd level depth for visibility_type = 'restricted'
    def test_subcategory_2_restricted_access_write_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.category_subcat_2.actual_visibility_parent_id.
             visibility_type), 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)
        self.assertFalse(self.category_subcat_1.visibility_group_ids)
        self.assertFalse(self.category_subcat_1.visibility_user_ids)
        self.assertFalse(self.category_subcat_2.visibility_group_ids)
        self.assertFalse(self.category_subcat_2.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

    def test_subcategory_2_restricted_access_write_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.category_subcat_2.actual_visibility_parent_id.
             visibility_type), 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)
        self.assertFalse(self.category_subcat_1.visibility_group_ids)
        self.assertFalse(self.category_subcat_1.visibility_user_ids)
        self.assertFalse(self.category_subcat_2.visibility_group_ids)
        self.assertFalse(self.category_subcat_2.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

    def test_subcategory_2_restricted_editors_access_write_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.category_subcat_2.actual_visibility_parent_id.
             visibility_type), 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)
        self.assertFalse(self.category_subcat_1.editor_group_ids)
        self.assertFalse(self.category_subcat_1.editor_user_ids)
        self.assertFalse(self.category_subcat_2.editor_group_ids)
        self.assertFalse(self.category_subcat_2.editor_user_ids)
        self.assertFalse(self.category_subcat_1.actual_editor_group_ids)
        self.assertFalse(self.category_subcat_1.actual_editor_user_ids)
        self.assertFalse(self.category_subcat_2.actual_editor_group_ids)
        self.assertFalse(self.category_subcat_2.actual_editor_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.editor_user_ids), 1)
        self.assertFalse(self.category_subcat_1.editor_group_ids)
        self.assertFalse(self.category_subcat_1.editor_user_ids)
        self.assertFalse(self.category_subcat_2.editor_group_ids)
        self.assertFalse(self.category_subcat_2.editor_user_ids)
        self.assertFalse(self.category_subcat_1.actual_editor_group_ids)
        self.assertEqual(len(self.category_subcat_1.actual_editor_user_ids), 1)
        self.assertFalse(self.category_subcat_2.actual_editor_group_ids)
        self.assertEqual(len(self.category_subcat_2.actual_editor_user_ids), 1)

        self.category_top_level.with_user(self.demo_user).write({
            'name': 'Top level category 1 renamed'})
        self.category_subcat_1.with_user(self.demo_user).write({
            'name': 'Top level category 1 renamed'})
        self.category_subcat_2.with_user(self.demo_user).write({
            'name': 'Top level category 1 renamed'})

    def test_subcategory_2_restricted_editors_access_write_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.category_subcat_2.actual_visibility_parent_id.
             visibility_type), 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)
        self.assertFalse(self.category_subcat_1.editor_group_ids)
        self.assertFalse(self.category_subcat_1.editor_user_ids)
        self.assertFalse(self.category_subcat_2.editor_group_ids)
        self.assertFalse(self.category_subcat_2.editor_user_ids)
        self.assertFalse(self.category_subcat_1.actual_editor_group_ids)
        self.assertFalse(self.category_subcat_1.actual_editor_user_ids)
        self.assertFalse(self.category_subcat_2.actual_editor_group_ids)
        self.assertFalse(self.category_subcat_2.actual_editor_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.editor_group_ids), 1)
        self.assertFalse(self.category_subcat_1.editor_group_ids)
        self.assertFalse(self.category_subcat_1.editor_user_ids)
        self.assertFalse(self.category_subcat_2.editor_group_ids)
        self.assertFalse(self.category_subcat_2.editor_user_ids)
        self.assertEqual(
            len(self.category_subcat_1.actual_editor_group_ids), 1)
        self.assertFalse(self.category_subcat_1.actual_editor_user_ids)
        self.assertEqual(
            len(self.category_subcat_2.actual_editor_group_ids), 1)
        self.assertFalse(self.category_subcat_2.actual_editor_user_ids)

        self.category_top_level.with_user(self.demo_user).write({
            'name': 'Top level category 1 renamed'})
        self.category_subcat_1.with_user(self.demo_user).write({
            'name': 'Top level category 1 renamed'})
        self.category_subcat_2.with_user(self.demo_user).write({
            'name': 'Top level category 1 renamed'})

    def test_subcategory_2_restricted_owners_access_write_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.category_subcat_2.actual_visibility_parent_id.
             visibility_type), 'restricted')
        self.assertFalse(self.category_top_level.owner_group_ids)
        self.assertEqual(len(self.category_top_level.owner_user_ids), 0)
        self.assertFalse(self.category_subcat_1.owner_group_ids)
        self.assertEqual(len(self.category_subcat_1.owner_user_ids), 0)
        self.assertFalse(self.category_subcat_2.owner_group_ids)
        self.assertEqual(len(self.category_subcat_2.owner_user_ids), 0)
        self.assertFalse(self.category_subcat_1.actual_owner_group_ids)
        self.assertEqual(len(self.category_subcat_1.actual_owner_user_ids), 0)
        self.assertFalse(self.category_subcat_2.actual_owner_group_ids)
        self.assertEqual(len(self.category_subcat_2.actual_owner_user_ids), 0)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).write({
                'name': 'Subcategory 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Subcategory 2 renamed'})

        self.category_top_level.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.owner_user_ids), 1)
        self.assertFalse(self.category_subcat_1.owner_group_ids)
        self.assertEqual(len(self.category_subcat_1.owner_user_ids), 0)
        self.assertFalse(self.category_subcat_2.owner_group_ids)
        self.assertEqual(len(self.category_subcat_2.owner_user_ids), 0)
        self.assertFalse(self.category_subcat_1.actual_owner_group_ids)
        self.assertEqual(len(self.category_subcat_1.actual_owner_user_ids), 1)
        self.assertFalse(self.category_subcat_2.actual_owner_group_ids)
        self.assertEqual(len(self.category_subcat_2.actual_owner_user_ids), 1)

        self.category_top_level.with_user(self.demo_user).write({
            'name': 'Top level category 1 renamed'})
        self.category_subcat_1.with_user(self.demo_user).write({
            'name': 'Subcategory 1 renamed'})
        self.category_subcat_2.with_user(self.demo_user).write({
            'name': 'Subcategory 2 renamed'})

    def test_subcategory_2_restricted_owners_access_write_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.category_subcat_2.actual_visibility_parent_id.
             visibility_type), 'restricted')
        self.assertFalse(self.category_top_level.owner_group_ids)
        self.assertEqual(len(self.category_top_level.owner_user_ids), 0)
        self.assertFalse(self.category_subcat_1.owner_group_ids)
        self.assertEqual(len(self.category_subcat_1.owner_user_ids), 0)
        self.assertFalse(self.category_subcat_2.owner_group_ids)
        self.assertEqual(len(self.category_subcat_2.owner_user_ids), 0)
        self.assertFalse(self.category_subcat_1.actual_owner_group_ids)
        self.assertEqual(len(self.category_subcat_1.actual_owner_user_ids), 0)
        self.assertFalse(self.category_subcat_2.actual_owner_group_ids)
        self.assertEqual(len(self.category_subcat_2.actual_owner_user_ids), 0)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).write({
                'name': 'Subcategory 1 renamed'})
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Subcategory 2 renamed'})

        self.category_top_level.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.owner_user_ids), 0)
        self.assertFalse(self.category_subcat_1.owner_group_ids)
        self.assertEqual(len(self.category_subcat_1.owner_user_ids), 0)
        self.assertFalse(self.category_subcat_2.owner_group_ids)
        self.assertEqual(len(self.category_subcat_2.owner_user_ids), 0)
        self.assertEqual(len(self.category_subcat_1.actual_owner_group_ids), 1)
        self.assertEqual(len(self.category_subcat_1.actual_owner_user_ids), 0)
        self.assertEqual(len(self.category_subcat_2.actual_owner_group_ids), 1)
        self.assertEqual(len(self.category_subcat_2.actual_owner_user_ids), 0)

        self.category_top_level.with_user(self.demo_user).write({
            'name': 'Top level category 1 renamed'})
        self.category_subcat_1.with_user(self.demo_user).write({
            'name': 'Subcategory 1 renamed'})
        self.category_subcat_2.with_user(self.demo_user).write({
            'name': 'Subcategory 2 renamed'})

    # Testing subcategory 2nd level depth for visibility_type = 'public'
    def test_subcategory_public_access_write_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.category_subcat_2.actual_visibility_parent_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'public'

        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

    # Testing subcategory 2nd level depth for visibility_type = 'portal'
    def test_subcategory_2_portal_access_write_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.category_subcat_2.actual_visibility_parent_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'portal'

        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

    # Testing subcategory 2nd level depth for visibility_type = 'internal'
    def test_subcategory_2_internal_access_read_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.category_subcat_2.actual_visibility_parent_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).write({
                'name': 'Top level category 1 renamed'})
