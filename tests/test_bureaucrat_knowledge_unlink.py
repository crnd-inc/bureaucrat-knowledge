from odoo.exceptions import AccessError
from .test_common import TestBureaucratKnowledgeBase


class TestKnowledgeCategoryDocumentUnlink(TestBureaucratKnowledgeBase):

    # Testing Top level category for visibility_type = 'restricted'
    def test_category_restricted_access_unlink_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

    def test_category_restricted_access_unlink_group(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

    def test_category_restricted_editors_access_unlink_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

        self.category_top_level.write({
            'editor_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.category_top_level.editor_user_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

    def test_category_restricted_editors_access_unlink_group(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

        self.category_top_level.write({
            'editor_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.category_top_level.editor_group_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

    def test_category_restricted_owners_access_unlink_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        Category = self.env['bureaucrat.knowledge.category']
        category = Category.create({
            'name': 'Test top level category'})

        self.assertEqual(category.visibility_type, 'restricted')
        self.assertFalse(category.owner_group_ids)
        self.assertEqual(len(category.owner_user_ids), 1)

        with self.assertRaises(AccessError):
            category.sudo(self.user).unlink()

        category.write({
            'owner_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(category.owner_user_ids), 2)
        category.sudo(self.user).unlink()

    def test_category_restricted_owners_access_write_group(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        Category = self.env['bureaucrat.knowledge.category']
        category = Category.create({
            'name': 'Test top level category'})

        self.assertEqual(category.visibility_type, 'restricted')
        self.assertFalse(category.owner_group_ids)
        self.assertEqual(len(category.owner_user_ids), 1)

        with self.assertRaises(AccessError):
            category.sudo(self.user).unlink()

        category.write({
            'owner_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(category.owner_group_ids), 1)
        category.sudo(self.user).unlink()

    # Testing Top level category for visibility_type = 'public'
    def test_category_public_access_unlink_user(self):
        self.public_user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

    # Testing Top level category for visibility_type = 'portal'
    def test_category_portal_access_unlink_user(self):
        self.portal_user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

    # Testing Top level category for visibility_type = 'internal'
    def test_category_internal_access_write_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

    # Testing subcategory 2nd level depth for visibility_type = 'restricted'
    def test_subcategory_2_restricted_access_unlink_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

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
            self.category_top_level.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.user).unlink()

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.user).unlink()

    def test_subcategory_2_restricted_access_unlink_group(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

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
            self.category_top_level.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.user).unlink()

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.user).unlink()

    def test_subcategory_2_restricted_editors_access_unlink_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

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
            self.category_top_level.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.user).unlink()

        self.category_top_level.write({
            'editor_user_ids': [(4, self.user.id)]})

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
            self.category_top_level.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.user).unlink()

    def test_subcategory_2_restricted_editors_access_write_group(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

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
            self.category_top_level.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.user).unlink()

        self.category_top_level.write({
            'editor_group_ids': [(4, self.group_employee.id)]})

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
            self.category_top_level.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_1.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.user).unlink()

    def test_subcategory_2_restricted_owners_access_unlink_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        Category = self.env['bureaucrat.knowledge.category']
        category_top_level = Category.create({
            'name': 'Test top level category '})
        category_subcat_1 = Category.create({
            'name': 'Test subcategory 1',
            'parent_id': category_top_level.id,
        })
        category_subcat_2 = Category.create({
            'name': 'Test subcategory 2',
            'parent_id': category_subcat_1.id,
        })

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
        self.assertEqual(len(category_top_level.owner_user_ids), 1)
        self.assertEqual(len(category_subcat_2.owner_user_ids), 1)

        with self.assertRaises(AccessError):
            category_subcat_2.sudo(self.user).unlink()

        self.category_subcat_2.write({
            'owner_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(category_top_level.owner_user_ids), 1)
        self.assertEqual(len(category_subcat_2.owner_user_ids), 1)
        category_subcat_2.sudo(self.user).unlink()
