from odoo.exceptions import AccessError
from .test_common import TestBureaucratKnowledgeBase


class TestKnowledgeCategoryUnlink(TestBureaucratKnowledgeBase):

    @classmethod
    def setUpClass(cls):
        super(TestKnowledgeCategoryUnlink, cls).setUpClass()
        cls.demo_user.groups_id |= cls.group_knowledge_user

    # Testing Top level category for visibility_type = 'restricted'
    def test_category_restricted_access_unlink_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

    def test_category_restricted_access_unlink_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

    def test_category_restricted_editors_access_unlink_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

        self.category_top_level.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.editor_user_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

    def test_category_restricted_editors_access_unlink_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

        self.category_top_level.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.editor_group_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

    def test_category_restricted_owners_access_unlink_user(self):
        Category = self.env['bureaucrat.knowledge.category']
        category = Category.create({
            'name': 'Test top level category',
            'code': 'top-10'})

        self.assertEqual(category.visibility_type, 'restricted')
        self.assertFalse(category.owner_group_ids)
        self.assertEqual(len(category.owner_user_ids), 0)

        with self.assertRaises(AccessError):
            category.with_user(self.demo_user).unlink()

        category.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(category.owner_user_ids), 1)
        category.with_user(self.demo_user).unlink()

    def test_category_restricted_owners_access_write_group(self):
        self.demo_user.groups_id |= self.group_demo

        Category = self.env['bureaucrat.knowledge.category']
        category = Category.create({
            'name': 'Test top level category',
            'code': 'top-11'})

        self.assertEqual(category.visibility_type, 'restricted')
        self.assertFalse(category.owner_group_ids)
        self.assertEqual(len(category.owner_user_ids), 0)

        with self.assertRaises(AccessError):
            category.with_user(self.demo_user).unlink()

        category.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(category.owner_group_ids), 1)
        category.with_user(self.demo_user).unlink()

    # Testing Top level category for visibility_type = 'public'
    def test_category_public_access_unlink_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

    # Testing Top level category for visibility_type = 'portal'
    def test_category_portal_access_unlink_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

    # Testing Top level category for visibility_type = 'internal'
    def test_category_internal_access_write_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

    # Testing subcategory 2nd level depth for visibility_type = 'restricted'
    def test_subcategory_2_restricted_access_unlink_user(self):
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
            self.category_top_level.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).unlink()

    def test_subcategory_2_restricted_access_unlink_group(self):
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
            self.category_top_level.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).unlink()

    def test_subcategory_2_restricted_editors_access_unlink_user(self):
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
            self.category_top_level.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).unlink()

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

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).unlink()

    def test_subcategory_2_restricted_editors_access_unlink_group(self):
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
            self.category_top_level.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).unlink()

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

        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.with_user(self.demo_user).unlink()

    def test_subcategory_2_restricted_owners_access_unlink_user(self):
        Category = self.env['bureaucrat.knowledge.category']
        category_top_level = Category.create({
            'name': 'Test top level category ',
            'code': 'top-15'})
        category_subcat_1 = Category.create({
            'name': 'Test subcategory 1',
            'code': 'top-16',
            'parent_id': category_top_level.id,
        })
        category_subcat_2 = Category.create({
            'name': 'Test subcategory 2',
            'code': 'top-17',
            'parent_id': category_subcat_1.id,
        })
        self.env['bureaucrat.knowledge.category']._parent_store_compute()

        self.assertEqual(
            category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            category_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (category_subcat_2.actual_visibility_parent_id.
             visibility_type), 'restricted')

        self.assertFalse(category_top_level.owner_group_ids)
        self.assertEqual(len(category_top_level.owner_user_ids), 0)
        self.assertFalse(category_subcat_1.owner_group_ids)
        self.assertEqual(len(category_subcat_1.owner_user_ids), 0)
        self.assertFalse(category_subcat_2.owner_group_ids)
        self.assertEqual(len(category_subcat_2.owner_user_ids), 0)
        self.assertFalse(category_subcat_1.actual_owner_group_ids)
        self.assertEqual(len(category_subcat_1.actual_owner_user_ids), 0)
        self.assertFalse(category_subcat_2.actual_owner_group_ids)
        self.assertEqual(len(category_subcat_2.actual_owner_user_ids), 0)

        with self.assertRaises(AccessError):
            category_subcat_2.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            category_subcat_1.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            category_top_level.with_user(self.demo_user).unlink()

        category_top_level.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(category_subcat_1.parent_id, category_top_level)
        self.assertEqual(category_subcat_2.parent_id, category_subcat_1)
        self.assertEqual(len(category_top_level.owner_user_ids), 1)
        self.assertFalse(category_subcat_1.owner_group_ids)
        self.assertEqual(len(category_subcat_1.owner_user_ids), 0)
        self.assertFalse(category_subcat_1.actual_owner_group_ids)
        self.assertEqual(len(category_subcat_1.actual_owner_user_ids), 1)
        self.assertFalse(category_subcat_2.owner_group_ids)
        self.assertEqual(len(category_subcat_2.owner_user_ids), 0)
        self.assertFalse(category_subcat_2.actual_owner_group_ids)
        self.assertEqual(len(category_subcat_2.actual_owner_user_ids), 1)

        category_subcat_2.with_user(self.demo_user).unlink()
        category_subcat_1.with_user(self.demo_user).unlink()
        category_top_level.with_user(self.demo_user).unlink()

    def test_subcategory_2_restricted_owners_access_unlink_group(self):
        self.demo_user.groups_id |= self.group_demo

        Category = self.env['bureaucrat.knowledge.category']
        category_top_level = Category.create({
            'name': 'Test top level category',
            'code': 'top-12'})
        category_subcat_1 = Category.create({
            'name': 'Test subcategory 1',
            'code': 'top-13',
            'parent_id': category_top_level.id,
        })
        category_subcat_2 = Category.create({
            'name': 'Test subcategory 2',
            'code': 'top-14',
            'parent_id': category_subcat_1.id,
        })
        self.env['bureaucrat.knowledge.category']._parent_store_compute()

        self.assertEqual(
            category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            category_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (category_subcat_2.actual_visibility_parent_id.
             visibility_type), 'restricted')

        self.assertFalse(category_top_level.owner_group_ids)
        self.assertEqual(len(category_top_level.owner_user_ids), 0)
        self.assertFalse(category_subcat_1.owner_group_ids)
        self.assertEqual(len(category_subcat_1.owner_user_ids), 0)
        self.assertFalse(category_subcat_2.owner_group_ids)
        self.assertEqual(len(category_subcat_2.owner_user_ids), 0)
        self.assertFalse(category_subcat_1.actual_owner_group_ids)
        self.assertEqual(len(category_subcat_1.actual_owner_user_ids), 0)
        self.assertFalse(category_subcat_2.actual_owner_group_ids)
        self.assertEqual(len(category_subcat_2.actual_owner_user_ids), 0)

        with self.assertRaises(AccessError):
            category_subcat_2.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            category_subcat_1.with_user(self.demo_user).unlink()
        with self.assertRaises(AccessError):
            category_top_level.with_user(self.demo_user).unlink()

        category_top_level.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(category_subcat_2.parent_id, category_subcat_1)
        self.assertEqual(len(category_top_level.owner_user_ids), 0)
        self.assertEqual(len(category_top_level.owner_group_ids), 1)
        self.assertFalse(category_subcat_1.owner_group_ids)
        self.assertEqual(len(category_subcat_1.owner_user_ids), 0)
        self.assertEqual(len(category_subcat_1.actual_owner_group_ids), 1)
        self.assertEqual(len(category_subcat_1.actual_owner_user_ids), 0)
        self.assertFalse(category_subcat_2.owner_group_ids)
        self.assertEqual(len(category_subcat_2.owner_user_ids), 0)
        self.assertEqual(len(category_subcat_1.actual_owner_user_ids), 0)
        self.assertEqual(len(category_subcat_2.actual_owner_group_ids), 1)

        # category_subcat_2.with_user(self.demo_user).unlink()
        category_subcat_1.with_user(self.demo_user).unlink()
        category_top_level.with_user(self.demo_user).unlink()

    # Testing subcategory 2nd level depth for visibility_type = 'public'
    def test_subcategory_public_access_unlink_user(self):
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
            self.category_subcat_2.with_user(self.public_user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.public_user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.public_user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.public_user).unlink()

    # Testing subcategory 2nd level depth for visibility_type = 'portal'
    def test_subcategory_2_portal_access_unlink_user(self):
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
            self.category_subcat_2.with_user(self.portal_user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.portal_user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.portal_user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.portal_user).unlink()

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
            self.category_subcat_2.with_user(self.portal_user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_subcat_1.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.with_user(self.demo_user).unlink()
