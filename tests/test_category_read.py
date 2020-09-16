from odoo.exceptions import AccessError
from .test_common import TestBureaucratKnowledgeBase


class TesteKnowledgeCategoryRead(TestBureaucratKnowledgeBase):

    # Testing Top level category for visibility_type = 'restricted'
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

    # Testing Top level category for visibility_type = 'public'
    def test_category_public_access_read_user(self):
        self.public_user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.public_user).read(['name'])

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.public_user).read(['name'])

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.public_user).read(['name'])

        self.category_top_level.visibility_type = 'public'

        self.assertEqual(
            self.category_top_level.sudo(self.public_user).name,
            'Top level category 1')

    # Testing Top level category for visibility_type = 'portal'
    def test_category_portal_access_read_user(self):
        self.portal_user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.public_user).read(['name'])

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.public_user).read(['name'])

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.public_user).read(['name'])

        self.category_top_level.visibility_type = 'portal'

        self.assertEqual(
            self.category_top_level.sudo(self.portal_user).name,
            'Top level category 1')

    # Testing Top level category for visibility_type = 'internal'
    def test_category_internal_access_read_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.public_user).read(['name'])

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.public_user).read(['name'])

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.public_user).read(['name'])

        self.category_top_level.visibility_type = 'internal'

        self.assertEqual(
            self.category_top_level.sudo(self.user).name,
            'Top level category 1')

    # Testing subcategory 2nd level depth for visibility_type = 'restricted'
    def test_subcategory_2_restricted_access_read_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)
        self.assertFalse(self.category_subcat_1.visibility_group_ids)
        self.assertFalse(self.category_subcat_1.visibility_user_ids)
        self.assertFalse(self.category_subcat_2.visibility_group_ids)
        self.assertFalse(self.category_subcat_2.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).read(['name'])
        with self.assertRaises(AccessError):
            self.category_subcat_1.sudo(self.user).read(['name'])
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.user).read(['name'])

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        self.assertEqual(
            self.category_top_level.sudo(self.user).name,
            'Top level category 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.user).name,
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.user).name,
            'Subcategory 2')

    def test_subcategory_2_restricted_access_read_group(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)
        self.assertFalse(self.category_subcat_1.visibility_group_ids)
        self.assertFalse(self.category_subcat_1.visibility_user_ids)
        self.assertFalse(self.category_subcat_2.visibility_group_ids)
        self.assertFalse(self.category_subcat_2.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).read(['name'])
        with self.assertRaises(AccessError):
            self.category_subcat_1.sudo(self.user).read(['name'])
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.user).read(['name'])

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        self.assertEqual(
            self.category_top_level.sudo(self.user).name,
            'Top level category 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.user).name,
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.user).name,
            'Subcategory 2')

    def test_subcategory_2_restricted_editors_access_read_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
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
            self.category_top_level.sudo(self.user).read(['name'])
        with self.assertRaises(AccessError):
            self.category_subcat_1.sudo(self.user).read(['name'])
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.user).read(['name'])

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

        self.assertEqual(
            self.category_top_level.sudo(self.user).name,
            'Top level category 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.user).name,
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.user).name,
            'Subcategory 2')

    def test_subcategory_2_restricted_editors_access_read_group(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
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
            self.category_top_level.sudo(self.user).read(['name'])
        with self.assertRaises(AccessError):
            self.category_subcat_1.sudo(self.user).read(['name'])
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.user).read(['name'])

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

        self.assertEqual(
            self.category_top_level.sudo(self.user).name,
            'Top level category 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.user).name,
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.user).name,
            'Subcategory 2')

    def test_subcategory_2_restricted_owners_access_read_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
        self.assertFalse(self.category_top_level.owner_group_ids)
        self.assertEqual(len(self.category_top_level.owner_user_ids), 1)
        self.assertEqual(len(self.category_subcat_2.owner_user_ids), 1)

        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.user).read(['name'])

        self.category_subcat_2.write({
            'owner_user_ids': [(4, self.user.id)]})

        self.assertEqual(len(self.category_top_level.owner_user_ids), 1)
        self.assertEqual(len(self.category_subcat_2.owner_user_ids), 2)
        self.assertEqual(
            self.category_subcat_2.sudo(self.user).name,
            'Subcategory 2')

    def test_subcategory_2_restricted_owners_access_read_group(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
        self.assertFalse(self.category_top_level.owner_group_ids)
        self.assertEqual(len(self.category_top_level.owner_user_ids), 1)
        self.assertFalse(self.category_subcat_2.owner_group_ids)

        with self.assertRaises(AccessError):
            self.category_top_level.sudo(self.user).read(['name'])

        self.category_subcat_2.write({
            'owner_group_ids': [(4, self.group_employee.id)]})

        self.assertEqual(len(self.category_subcat_2.owner_group_ids), 1)
        self.assertEqual(
            self.category_subcat_2.sudo(self.user).name,
            'Subcategory 2')

    # Testing subcategory 2nd level depth for visibility_type = 'public'
    def test_subcategory_public_access_read_user(self):
        self.public_user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')

        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.public_user).read(['name'])

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.public_user).read(['name'])

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.public_user).read(['name'])

        self.category_top_level.visibility_type = 'public'

        self.assertEqual(
            self.category_subcat_2.sudo(self.public_user).name,
            'Subcategory 2')

    # Testing subcategory 2nd level depth for visibility_type = 'portal'
    def test_subcategory_2_portal_access_read_user(self):
        self.portal_user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')

        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.portal_user).read(['name'])

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.portal_user).read(['name'])

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.portal_user).read(['name'])

        self.category_top_level.visibility_type = 'portal'

        self.assertEqual(
            self.category_subcat_2.sudo(self.portal_user).name,
            'Subcategory 2')

    # Testing subcategory 2nd level depth for visibility_type = 'internal'
    def test_subcategory_2_internal_access_read_user(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')

        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.public_user).read(['name'])

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.public_user).read(['name'])

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.category_subcat_2.sudo(self.public_user).read(['name'])

        self.category_top_level.visibility_type = 'internal'

        self.assertEqual(
            self.category_subcat_2.sudo(self.user).name,
            'Subcategory 2')
