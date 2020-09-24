# pylint: disable= too-many-lines
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

    def test_subcategory_2_restricted_editors_access_unlink_group(self):
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
        self.assertFalse(category_subcat_1.owner_group_ids)
        self.assertEqual(len(category_subcat_1.owner_user_ids), 1)
        self.assertFalse(category_subcat_2.owner_group_ids)
        self.assertEqual(len(category_subcat_2.owner_user_ids), 1)
        self.assertFalse(category_subcat_1.actual_owner_group_ids)
        self.assertEqual(len(category_subcat_1.actual_owner_user_ids), 1)
        self.assertFalse(category_subcat_2.actual_owner_group_ids)
        self.assertEqual(len(category_subcat_2.actual_owner_user_ids), 1)

        with self.assertRaises(AccessError):
            category_subcat_2.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            category_subcat_1.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            category_top_level.sudo(self.user).unlink()

        self.category_top_level.invalidate_cache()
        self.category_subcat_1.invalidate_cache()
        self.category_subcat_2.invalidate_cache()
        category_top_level.write({
            'owner_user_ids': [(4, self.user.id)]})

        self.assertEqual(category_subcat_1.parent_id, category_top_level)
        self.assertEqual(category_subcat_2.parent_id, category_subcat_1)
        self.assertEqual(len(category_top_level.owner_user_ids), 2)
        self.assertFalse(category_subcat_1.owner_group_ids)
        self.assertEqual(len(category_subcat_1.owner_user_ids), 1)
        self.assertFalse(category_subcat_1.actual_owner_group_ids)
        self.category_top_level.invalidate_cache()
        self.category_subcat_1.invalidate_cache()
        self.category_subcat_2.invalidate_cache()
        self.assertEqual(len(category_subcat_1.actual_owner_user_ids), 2)
        self.assertFalse(category_subcat_2.owner_group_ids)
        self.assertEqual(len(category_subcat_2.owner_user_ids), 1)
        self.assertFalse(category_subcat_2.actual_owner_group_ids)

        # TODO: find out why self.user.id
        # not assigned to category_subcat_2.actual_owner_user_ids
        self.assertEqual(len(category_subcat_2.actual_owner_user_ids), 2)

        category_subcat_2.sudo(self.user).unlink()
        category_subcat_1.sudo(self.user).unlink()
        category_top_level.sudo(self.user).unlink()

    def test_subcategory_2_restricted_owners_access_unlink_group(self):
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
        self.assertFalse(category_subcat_1.owner_group_ids)
        self.assertEqual(len(category_subcat_1.owner_user_ids), 1)
        self.assertFalse(category_subcat_2.owner_group_ids)
        self.assertEqual(len(category_subcat_2.owner_user_ids), 1)
        self.assertFalse(category_subcat_1.actual_owner_group_ids)
        self.assertEqual(len(category_subcat_1.actual_owner_user_ids), 1)
        self.assertFalse(category_subcat_2.actual_owner_group_ids)
        self.assertEqual(len(category_subcat_2.actual_owner_user_ids), 1)

        with self.assertRaises(AccessError):
            category_subcat_2.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            category_subcat_1.sudo(self.user).unlink()
        with self.assertRaises(AccessError):
            category_top_level.sudo(self.user).unlink()

        category_top_level.write({
            'owner_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(category_subcat_2.parent_id, category_subcat_1)
        self.assertEqual(len(category_top_level.owner_user_ids), 1)
        self.assertEqual(len(category_top_level.owner_group_ids), 1)
        self.assertFalse(category_subcat_1.owner_group_ids)
        self.assertEqual(len(category_subcat_1.owner_user_ids), 1)
        self.assertEqual(len(category_subcat_1.actual_owner_group_ids), 1)
        self.assertEqual(len(category_subcat_1.actual_owner_user_ids), 1)
        self.assertFalse(category_subcat_2.owner_group_ids)
        self.assertEqual(len(category_subcat_2.owner_user_ids), 1)
        self.assertEqual(len(category_subcat_1.actual_owner_user_ids), 1)

        # TODO: find out why self.group_employee.id
        # not assigned to category_subcat_2.actual_owner_group_ids
        # self.assertEqual(len(category_subcat_2.actual_owner_group_ids), 1)

        # category_subcat_2.sudo(self.user).unlink()
        category_subcat_1.sudo(self.user).unlink()
        category_top_level.sudo(self.user).unlink()

    # Testing subcategory 2nd level depth for visibility_type = 'public'
    def test_subcategory_public_access_unlink_user(self):
        self.public_user.groups_id |= self.group_knowledge_user_implicit

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
            self.category_subcat_2.sudo(self.public_user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_subcat_1.sudo(self.public_user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.public_user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.public_user).unlink()

    # Testing subcategory 2nd level depth for visibility_type = 'portal'
    def test_subcategory_2_portal_access_unlink_user(self):
        self.portal_user.groups_id |= self.group_knowledge_user_implicit

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
            self.category_subcat_2.sudo(self.portal_user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_subcat_1.sudo(self.portal_user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.portal_user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.portal_user).unlink()

    # Testing subcategory 2nd level depth for visibility_type = 'internal'
    def test_subcategory_2_internal_access_read_user(self):
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

        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.portal_user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_subcat_1.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).unlink()

    # Testing document
    def test_document_restricted_access_unlink_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertFalse(self.document_subcat_2.visibility_group_ids)
        self.assertFalse(self.document_subcat_2.visibility_user_ids)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'visibility_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.document_subcat_2.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

    def test_document_restricted_access_unlink_group(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertFalse(self.document_subcat_2.visibility_group_ids)
        self.assertFalse(self.document_subcat_2.visibility_user_ids)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.write({
            'visibility_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.document_subcat_2.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

    def test_document_restricted_editors_access_unlink_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertFalse(self.document_subcat_2.editor_group_ids)
        self.assertFalse(self.document_subcat_2.editor_user_ids)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.write({
            'editor_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.document_subcat_2.editor_user_ids), 1)

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

    def test_document_restricted_editors_access_unlink_group(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertFalse(self.document_subcat_2.editor_group_ids)
        self.assertFalse(self.document_subcat_2.editor_user_ids)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.write({
            'editor_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.document_subcat_2.editor_group_ids), 1)

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

    def test_document_restricted_owners_access_unlink_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        Document = self.env['bureaucrat.knowledge.document']
        document = Document.create({
            'name': 'Test document',
        })

        self.assertFalse(document.owner_group_ids)
        self.assertEqual(len(document.owner_user_ids), 1)

        document.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            document.sudo(self.user).unlink()

        document.write({
            'owner_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(document.owner_user_ids), 2)
        document.sudo(self.user).unlink()

    def test_document_restricted_owners_access_unlink_group(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        Document = self.env['bureaucrat.knowledge.document']
        document = Document.create({
            'name': 'Test document',
        })

        self.assertFalse(document.owner_group_ids)
        self.assertEqual(len(document.owner_user_ids), 1)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            document.sudo(self.user).unlink()

        document.write({
            'owner_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(document.owner_group_ids), 1)
        document.sudo(self.user).unlink()

    # Testing document visibility_type = 'public'
    def test_document_public_access_unlink_user(self):
        self.public_user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

    # Testing document visibility_type = 'public' from parent category
    def test_parent_document_public_access_unlink_user(self):
        self.public_user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

    # Testing document visibility_type = 'portal'
    def test_document_portal_access_unlink_user(self):
        self.portal_user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

    # Testing document visibility_type = 'portal' from parent category
    def test_parent_document_portal_access_unlink_user(self):
        self.portal_user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.portal_user).unlink()

        self.category_top_level.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.portal_user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.portal_user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.portal_user).unlink()

        self.document_subcat_2.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.portal_user).unlink()

    # Testing document visibility_type = 'internal'
    def test_document_internal_access_unlink_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

    # Testing document visibility_type = 'internal' from parent category
    def test_parent_document_internal_access_unlink_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.document_subcat_2.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

    # Testing document with categoy, for visibility_type = 'restricted'
    def test_document_subcategory_2_restricted_access_unlink_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')
        self.assertFalse(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_group_ids))
        self.assertFalse(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_user_ids))
        self.assertFalse(self.document_subcat_2.visibility_group_ids)
        self.assertFalse(self.document_subcat_2.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_visibility_category_id.
                 visibility_user_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

    def test_document_subcategory_2_restricted_access_unlink_group(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')
        self.assertFalse(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_group_ids))
        self.assertFalse(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_user_ids))
        self.assertFalse(self.document_subcat_2.visibility_group_ids)
        self.assertFalse(self.document_subcat_2.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_visibility_category_id.
                 visibility_group_ids)), 1)

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

    def test_document_subcategory_2_restricted_editors_access_unlink_user(
            self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')
        self.assertFalse(
            (self.document_subcat_2.actual_visibility_category_id.
             editor_group_ids))
        self.assertFalse(
            (self.document_subcat_2.actual_visibility_category_id.
             editor_user_ids))
        self.assertFalse(self.document_subcat_2.editor_group_ids)
        self.assertFalse(self.document_subcat_2.editor_user_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_group_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_user_ids)

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.category_top_level.write({
            'editor_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.category_top_level.editor_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_user_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.category_top_level.write({
            'editor_user_ids': [(3, self.user.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        # Test editor subategory 1
        self.assertFalse(self.category_subcat_1.editor_user_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_user_ids)

        self.category_subcat_1.write({
            'editor_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.category_subcat_1.editor_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_user_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.category_subcat_1.write({
            'editor_user_ids': [(3, self.user.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        # Test editor subategory 2
        self.assertFalse(self.category_subcat_1.editor_user_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_user_ids)

        self.category_subcat_2.write({
            'editor_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.category_subcat_2.editor_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_user_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.category_subcat_2.write({
            'editor_user_ids': [(3, self.user.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

    def test_document_subcategory_2_restricted_editors_access_unlink_group(
            self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')
        self.assertFalse(
            (self.document_subcat_2.actual_visibility_category_id.
             editor_group_ids))
        self.assertFalse(
            (self.document_subcat_2.actual_visibility_category_id.
             editor_user_ids))
        self.assertFalse(self.document_subcat_2.editor_group_ids)
        self.assertFalse(self.document_subcat_2.editor_user_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_group_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_user_ids)

        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.category_top_level.write({
            'editor_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.category_top_level.editor_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_visibility_category_id.
                 editor_group_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.category_top_level.write({
            'editor_group_ids': [(3, self.group_employee.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        # Test editor subategory 1
        self.assertFalse(self.category_subcat_1.editor_group_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_group_ids)

        self.category_subcat_1.write({
            'editor_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.category_subcat_1.editor_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_group_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()
        self.document_subcat_2.sudo(self.user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

        self.category_subcat_1.write({
            'editor_group_ids': [(3, self.group_employee.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        # Test editor subategory 2
        self.assertFalse(self.category_subcat_2.editor_group_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_group_ids)

        self.category_subcat_2.write({
            'editor_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.category_subcat_2.editor_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_group_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        self.category_subcat_2.write({
            'editor_group_ids': [(3, self.group_employee.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

    def test_document_subcategory_2_restricted_owners_access_unlink_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        # TODO: find out why self.user.id
        # not assigned to category_subcat_2.actual_owner_user_ids
        # when category created in this method

        Document = self.env['bureaucrat.knowledge.document']
        document_subcat_2 = Document.create({
            'name': 'Test document',
            'category_id': self.category_subcat_2.id,
        })

        self.assertEqual(
            document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')
        self.assertFalse(
            (document_subcat_2.actual_visibility_category_id.
             owner_group_ids))
        self.assertEqual(
            len(document_subcat_2.actual_visibility_category_id.
                owner_user_ids), 1)
        self.assertFalse(document_subcat_2.owner_group_ids)
        self.assertEqual(len(document_subcat_2.owner_user_ids), 1)
        self.assertFalse(document_subcat_2.actual_owner_group_ids)
        self.assertEqual(len(document_subcat_2.actual_owner_user_ids), 1)

        with self.assertRaises(AccessError):
            document_subcat_2.sudo(self.user).unlink()

        # Add owner to Top level category
        self.category_top_level.write({
            'owner_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.category_top_level.owner_user_ids), 2)
        self.assertEqual(
            len((document_subcat_2.actual_owner_user_ids)), 2)
        document_subcat_2.sudo(self.user).unlink()

        self.category_top_level.write({
            'owner_user_ids': [(3, self.user.id)]})

        document_subcat_2 = Document.create({
            'name': 'Test document',
            'category_id': self.category_subcat_2.id,
        })
        with self.assertRaises(AccessError):
            self.document_subcat_2.sudo(self.user).unlink()

        # Test owner subategory 1
        self.assertEqual(len(self.category_subcat_1.owner_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_user_ids)), 1)

        self.category_subcat_1.write({
            'owner_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.category_subcat_1.owner_user_ids), 2)
        self.assertEqual(
            len((document_subcat_2.actual_owner_user_ids)), 2)
        document_subcat_2.sudo(self.user).unlink()

        self.category_subcat_1.write({
            'owner_user_ids': [(3, self.user.id)]})

        document_subcat_2 = Document.create({
            'name': 'Test document',
            'category_id': self.category_subcat_2.id,
        })
        with self.assertRaises(AccessError):
            document_subcat_2.sudo(self.user).unlink()

        # Test owner subategory 2
        self.assertEqual(len(self.category_subcat_2.owner_user_ids), 1)
        self.assertEqual(
            len((document_subcat_2.actual_owner_user_ids)), 1)

        self.category_subcat_2.write({
            'owner_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.category_subcat_2.owner_user_ids), 2)
        self.assertEqual(
            len((document_subcat_2.actual_owner_user_ids)), 2)
        document_subcat_2.sudo(self.user).unlink()

        self.category_subcat_2.write({
            'owner_user_ids': [(3, self.user.id)]})

        document_subcat_2 = Document.create({
            'name': 'Test document',
            'category_id': self.category_subcat_2.id,
        })
        with self.assertRaises(AccessError):
            document_subcat_2.sudo(self.user).unlink()

    def test_document_subcategory_2_restricted_owners_access_unlink_group(
            self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        # TODO: find out why self.group_employee.id
        # not assigned to category_subcat_2.actual_owner_group_ids
        # when category created in this method

        Document = self.env['bureaucrat.knowledge.document']
        document_subcat_2 = Document.create({
            'name': 'Test document',
            'category_id': self.category_subcat_2.id,
        })

        self.assertEqual(
            document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')
        self.assertFalse(
            (document_subcat_2.actual_visibility_category_id.
             owner_group_ids))
        self.assertEqual(
            len(document_subcat_2.actual_visibility_category_id.
                owner_user_ids), 1)
        self.assertFalse(document_subcat_2.owner_group_ids)
        self.assertEqual(len(document_subcat_2.owner_user_ids), 1)
        self.assertFalse(document_subcat_2.actual_owner_group_ids)
        self.assertEqual(len(document_subcat_2.actual_owner_user_ids), 1)

        with self.assertRaises(AccessError):
            document_subcat_2.sudo(self.user).unlink()

        # Add owner group to Top level category
        self.category_top_level.write({
            'owner_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.category_top_level.owner_group_ids), 1)
        self.assertEqual(
            len((document_subcat_2.actual_owner_group_ids)), 1)
        document_subcat_2.sudo(self.user).unlink()

        self.category_top_level.write({
            'owner_group_ids': [(3, self.group_employee.id)]})

        document_subcat_2 = Document.create({
            'name': 'Test document',
            'category_id': self.category_subcat_2.id,
        })
        with self.assertRaises(AccessError):
            document_subcat_2.sudo(self.user).unlink()

        # Test owner group subategory 1
        self.assertFalse(self.category_subcat_1.owner_group_ids)
        self.assertFalse(document_subcat_2.actual_owner_group_ids)

        self.category_subcat_1.write({
            'owner_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.category_subcat_1.owner_group_ids), 1)
        self.assertEqual(
            len((document_subcat_2.actual_owner_group_ids)), 1)
        document_subcat_2.sudo(self.user).unlink()

        self.category_subcat_1.write({
            'owner_group_ids': [(3, self.group_employee.id)]})

        document_subcat_2 = Document.create({
            'name': 'Test document',
            'category_id': self.category_subcat_2.id,
        })
        with self.assertRaises(AccessError):
            document_subcat_2.sudo(self.user).unlink()

        # Test owner group subategory 2
        self.assertFalse(self.category_subcat_1.owner_group_ids)
        self.assertFalse(document_subcat_2.actual_owner_group_ids)

        self.category_subcat_2.write({
            'owner_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.category_subcat_2.owner_group_ids), 1)
        self.assertEqual(
            len((document_subcat_2.actual_owner_group_ids)), 1)
        document_subcat_2.sudo(self.user).unlink()

        self.category_subcat_2.write({
            'owner_group_ids': [(3, self.group_employee.id)]})

        document_subcat_2 = Document.create({
            'name': 'Test document',
            'category_id': self.category_subcat_2.id,
        })
        with self.assertRaises(AccessError):
            document_subcat_2.sudo(self.user).unlink()
