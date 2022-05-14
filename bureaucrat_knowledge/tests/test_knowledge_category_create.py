from odoo.exceptions import AccessError
from .test_common import TestBureaucratKnowledgeBase


class TestKnowledgeCategoryCreate(TestBureaucratKnowledgeBase):

    @classmethod
    def setUpClass(cls):
        super(TestKnowledgeCategoryCreate, cls).setUpClass()
        cls.demo_user.groups_id |= cls.group_knowledge_user

    # Testing Top level category for visibility_type = 'restricted'
    def test_category_restricted_access_create_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

    def test_category_restricted_access_create_user2(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id,
                'owner_user_ids': [(4, self.demo_user.id)]})

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id,
                'owner_user_ids': [(4, self.demo_user.id)]})

    def test_category_restricted_access_create_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

    def test_category_restricted_editors_access_create_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)

        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

        self.category_top_level.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.editor_user_ids), 1)
        category = self.Category.with_user(self.demo_user).create({
            'name': 'Test Create',
            'parent_id': self.category_top_level.id})
        self.assertEqual(category.visibility_type, 'parent')
        self.assertFalse(category.visibility_user_ids)
        self.assertFalse(category.visibility_group_ids)
        self.assertFalse(category.editor_group_ids)
        self.assertFalse(category.editor_user_ids)
        self.assertFalse(category.owner_group_ids)
        self.assertFalse(category.owner_user_ids)

    def test_category_restricted_editors_access_create_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)

        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

        self.category_top_level.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.editor_group_ids), 1)
        category = self.Category.with_user(self.demo_user).create({
            'name': 'Test Create',
            'parent_id': self.category_top_level.id})
        self.assertEqual(category.visibility_type, 'parent')
        self.assertFalse(category.visibility_user_ids)
        self.assertFalse(category.visibility_group_ids)
        self.assertFalse(category.editor_group_ids)
        self.assertFalse(category.editor_user_ids)
        self.assertFalse(category.owner_group_ids)
        self.assertFalse(category.owner_user_ids)

    def test_category_restricted_owners_access_create_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.owner_group_ids)
        self.assertEqual(len(self.category_top_level.owner_user_ids), 0)

        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

        self.category_top_level.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.owner_user_ids), 1)
        category = self.Category.with_user(self.demo_user).create({
            'name': 'Test Create',
            'parent_id': self.category_top_level.id})
        self.assertEqual(category.visibility_type, 'parent')
        self.assertFalse(category.visibility_user_ids)
        self.assertFalse(category.visibility_group_ids)
        self.assertFalse(category.editor_group_ids)
        self.assertFalse(category.editor_user_ids)
        self.assertFalse(category.owner_group_ids)
        self.assertFalse(category.owner_user_ids)

    def test_category_restricted_owners_access_create_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.owner_group_ids)
        self.assertEqual(len(self.category_top_level.owner_user_ids), 0)

        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

        self.category_top_level.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.owner_group_ids), 1)
        category = self.Category.with_user(self.demo_user).create({
            'name': 'Test Create',
            'parent_id': self.category_top_level.id})
        self.assertEqual(category.visibility_type, 'parent')
        self.assertFalse(category.visibility_user_ids)
        self.assertFalse(category.visibility_group_ids)
        self.assertFalse(category.editor_group_ids)
        self.assertFalse(category.editor_user_ids)
        self.assertFalse(category.owner_group_ids)
        self.assertFalse(category.owner_user_ids)

    def test_category_create_top_level(self):
        category = self.Category.with_user(self.demo_user).create({
            'name': 'Test Create'})
        self.assertEqual(category.visibility_type, 'restricted')
        self.assertFalse(category.visibility_user_ids)
        self.assertFalse(category.visibility_group_ids)
        self.assertFalse(category.editor_group_ids)
        self.assertFalse(category.editor_user_ids)
        self.assertFalse(category.owner_group_ids)
        self.assertIn(self.demo_user, category.owner_user_ids)

    # Testing Top level category for visibility_type = 'public'
    def test_category_public_access_create_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')

        with self.assertRaises(AccessError):
            self.Category.with_user(self.public_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.Category.with_user(self.public_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.Category.with_user(self.public_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

        self.category_top_level.visibility_type = 'public'

        with self.assertRaises(AccessError):
            self.Category.with_user(self.public_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

    # Testing Top level category for visibility_type = 'portal'
    def test_category_portal_access_create_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')

        with self.assertRaises(AccessError):
            self.Category.with_user(self.portal_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.Category.with_user(self.portal_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.Category.with_user(self.portal_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.Category.with_user(self.portal_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

    # Testing Top level category for visibility_type = 'internal'
    def test_category_internal_access_create_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')

        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

        self.category_top_level.visibility_type = 'internal'

        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create',
                'parent_id': self.category_top_level.id})

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
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

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
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

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
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

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

        category = self.Category.with_user(self.demo_user).create({
            'name': 'Test Create Sub 1',
            'parent_id': self.category_subcat_2.id})
        self.assertEqual(category.visibility_type, 'parent')
        self.assertFalse(category.visibility_user_ids)
        self.assertFalse(category.visibility_group_ids)
        self.assertFalse(category.editor_group_ids)
        self.assertFalse(category.editor_user_ids)
        self.assertFalse(category.owner_group_ids)
        self.assertFalse(category.owner_user_ids)

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
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

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

        category = self.Category.with_user(self.demo_user).create({
            'name': 'Test Create Sub 1',
            'parent_id': self.category_subcat_2.id})
        self.assertEqual(category.visibility_type, 'parent')
        self.assertFalse(category.visibility_user_ids)
        self.assertFalse(category.visibility_group_ids)
        self.assertFalse(category.editor_group_ids)
        self.assertFalse(category.editor_user_ids)
        self.assertFalse(category.owner_group_ids)
        self.assertFalse(category.owner_user_ids)

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
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

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

        category = self.Category.with_user(self.demo_user).create({
            'name': 'Test Create Sub 1',
            'parent_id': self.category_subcat_2.id})
        self.assertEqual(category.visibility_type, 'parent')
        self.assertFalse(category.visibility_user_ids)
        self.assertFalse(category.visibility_group_ids)
        self.assertFalse(category.editor_group_ids)
        self.assertFalse(category.editor_user_ids)
        self.assertFalse(category.owner_group_ids)
        self.assertFalse(category.owner_user_ids)

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
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

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

        category = self.Category.with_user(self.demo_user).create({
            'name': 'Test Create Sub 1',
            'parent_id': self.category_subcat_2.id})
        self.assertEqual(category.visibility_type, 'parent')
        self.assertFalse(category.visibility_user_ids)
        self.assertFalse(category.visibility_group_ids)
        self.assertFalse(category.editor_group_ids)
        self.assertFalse(category.editor_user_ids)
        self.assertFalse(category.owner_group_ids)
        self.assertFalse(category.owner_user_ids)

    # Testing subcategory 2nd level depth for visibility_type = 'public'
    def test_subcategory_public_access_create_user(self):
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
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

        self.category_top_level.visibility_type = 'public'

        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

    # Testing subcategory 2nd level depth for visibility_type = 'portal'
    def test_subcategory_2_portal_access_create_user(self):
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
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

        self.category_top_level.visibility_type = 'portal'

        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

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
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.Category.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'parent_id': self.category_subcat_2.id})
