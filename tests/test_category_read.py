from odoo.exceptions import AccessError
from .test_common import TestBureaucratKnowledgeBase


class TesteKnowledgeCategoryRead(TestBureaucratKnowledgeBase):

    def test_category_restricted_access_read_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).read(['name'])

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        self.assertEqual(
            self.category_top_level.sudo(self.user).name,
            'Top level category 1')

    def test_category_restricted_access_read_group(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).read(['name'])

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        self.assertEqual(
            self.category_top_level.sudo(self.user).name,
            'Top level category 1')

    def test_category_restricted_editors_access_read_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).read(['name'])

        self.category_top_level.write({
            'editor_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.category_top_level.editor_user_ids), 1)
        self.assertEqual(
            self.category_top_level.sudo(self.user).name,
            'Top level category 1')

    def test_category_restricted_editors_access_read_group(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).read(['name'])

        self.category_top_level.write({
            'editor_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.category_top_level.editor_group_ids), 1)
        self.assertEqual(
            self.category_top_level.sudo(self.user).name,
            'Top level category 1')

    def test_category_restricted_owners_access_read_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.owner_group_ids)
        self.assertEqual(len(self.category_top_level.owner_user_ids), 1)

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).read(['name'])

        self.category_top_level.write({
            'owner_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.category_top_level.owner_user_ids), 2)
        self.assertEqual(
            self.category_top_level.sudo(self.user).name,
            'Top level category 1')

    def test_category_restricted_owners_access_read_group(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.owner_group_ids)
        self.assertEqual(len(self.category_top_level.owner_user_ids), 1)

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).read(['name'])

        self.category_top_level.write({
            'owner_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.category_top_level.owner_group_ids), 1)
        self.assertEqual(
            self.category_top_level.sudo(self.user).name,
            'Top level category 1')
