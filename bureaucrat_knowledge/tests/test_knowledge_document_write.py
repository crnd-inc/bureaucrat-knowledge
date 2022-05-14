from odoo.exceptions import AccessError
from .test_common import TestBureaucratKnowledgeBase


class TestKnowledgeDocumentWrite(TestBureaucratKnowledgeBase):

    @classmethod
    def setUpClass(cls):
        super(TestKnowledgeDocumentWrite, cls).setUpClass()
        cls.demo_user.groups_id |= cls.group_knowledge_user

    # Testing document
    def test_document_restricted_access_write_user(self):
        self.assertFalse(self.document_subcat_2.visibility_group_ids)
        self.assertFalse(self.document_subcat_2.visibility_user_ids)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.document_subcat_2.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

    def test_document_restricted_access_write_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertFalse(self.document_subcat_2.visibility_group_ids)
        self.assertFalse(self.document_subcat_2.visibility_user_ids)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.document_subcat_2.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

    def test_document_restricted_editors_access_write_user(self):
        self.assertFalse(self.document_subcat_2.editor_group_ids)
        self.assertFalse(self.document_subcat_2.editor_user_ids)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.document_subcat_2.editor_user_ids), 1)

        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

    def test_document_restricted_editors_access_write_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertFalse(self.document_subcat_2.editor_group_ids)
        self.assertFalse(self.document_subcat_2.editor_user_ids)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.document_subcat_2.editor_group_ids), 1)

        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

    def test_document_restricted_owners_access_write_user(self):
        self.assertFalse(self.document_subcat_2.owner_group_ids)
        self.assertEqual(len(self.document_subcat_2.owner_user_ids), 0)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.document_subcat_2.owner_user_ids), 1)
        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

    def test_document_restricted_owners_access_write_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertFalse(self.document_subcat_2.owner_group_ids)
        self.assertEqual(len(self.document_subcat_2.owner_user_ids), 0)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.document_subcat_2.owner_group_ids), 1)
        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

    # Testing document visibility_type = 'public'
    def test_document_public_access_write_user(self):
        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.public_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.public_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.public_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.public_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.public_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

    # Testing document visibility_type = 'public' from parent category
    def test_parent_document_public_access_write_user(self):
        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.public_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.category_top_level.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.public_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.public_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.public_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.public_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

    # Testing document visibility_type = 'portal'
    def test_document_portal_access_write_user(self):
        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.portal_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.portal_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.portal_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.portal_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.portal_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

    # Testing document visibility_type = 'portal' from parent category
    def test_parent_document_portal_access_write_user(self):
        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.portal_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.category_top_level.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.portal_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.portal_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.portal_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.portal_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

    # Testing document visibility_type = 'internal'
    def test_document_internal_access_write_user(self):
        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

    # Testing document visibility_type = 'internal' from parent category
    def test_parent_document_internal_access_write_user(self):
        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.category_top_level.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

    # Testing document with categoy, for visibility_type = 'restricted'
    def test_document_subcategory_2_restricted_access_write_user(self):
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
            self.document_subcat_2.with_user(self.demo_user).read(['name'])
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_visibility_category_id.
                 visibility_user_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

    def test_document_subcategory_2_restricted_access_write_group(self):
        self.demo_user.groups_id |= self.group_demo

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
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_visibility_category_id.
                 visibility_group_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

    def test_document_subcategory_2_restricted_editors_access_write_user(self):
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
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.category_top_level.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.editor_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_user_ids)), 1)
        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'name': 'Demo Document For Subcategory 2'})
        self.category_top_level.write({
            'editor_user_ids': [(3, self.demo_user.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        # Test editor subategory 1
        self.assertFalse(self.category_subcat_1.editor_user_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_user_ids)

        self.category_subcat_1.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_subcat_1.editor_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_user_ids)), 1)
        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'name': 'Demo Document For Subcategory 2'})
        self.category_subcat_1.write({
            'editor_user_ids': [(3, self.demo_user.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        # Test editor subategory 2
        self.assertFalse(self.category_subcat_1.editor_user_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_user_ids)

        self.category_subcat_2.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_subcat_2.editor_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_user_ids)), 1)
        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'name': 'Demo Document For Subcategory 2'})
        self.category_subcat_2.write({
            'editor_user_ids': [(3, self.demo_user.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

    def test_document_subcategory_2_restricted_editors_access_write_group(
            self):
        self.demo_user.groups_id |= self.group_demo

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
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        self.category_top_level.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.editor_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_visibility_category_id.
                 editor_group_ids)), 1)
        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'name': 'Demo Document For Subcategory 2'})
        self.category_top_level.write({
            'editor_group_ids': [(3, self.group_demo.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        # Test editor subategory 1
        self.assertFalse(self.category_subcat_1.editor_group_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_group_ids)

        self.category_subcat_1.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_subcat_1.editor_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_group_ids)), 1)
        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'name': 'Demo Document For Subcategory 2'})
        self.category_subcat_1.write({
            'editor_group_ids': [(3, self.group_demo.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        # Test editor subategory 2
        self.assertFalse(self.category_subcat_2.editor_group_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_group_ids)

        self.category_subcat_2.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_subcat_2.editor_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_group_ids)), 1)
        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'name': 'Demo Document For Subcategory 2'})
        self.category_subcat_2.write({
            'editor_group_ids': [(3, self.group_demo.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

    def test_document_subcategory_2_restricted_owners_access_write_user(self):
        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')
        self.assertFalse(
            (self.document_subcat_2.actual_visibility_category_id.
             owner_group_ids))
        self.assertEqual(
            len(self.document_subcat_2.actual_visibility_category_id.
                owner_user_ids), 0)
        self.assertFalse(self.document_subcat_2.owner_group_ids)
        self.assertEqual(len(self.document_subcat_2.owner_user_ids), 0)
        self.assertFalse(self.document_subcat_2.actual_owner_group_ids)
        self.assertEqual(len(self.document_subcat_2.actual_owner_user_ids), 0)

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        # Add owner to Top level category
        self.category_top_level.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.owner_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_user_ids)), 1)
        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'name': 'Demo Document For Subcategory 2'})
        self.category_top_level.write({
            'owner_user_ids': [(3, self.demo_user.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        # Test owner subategory 1
        self.assertEqual(len(self.category_subcat_1.owner_user_ids), 0)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_user_ids)), 0)

        self.category_subcat_1.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_subcat_1.owner_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_user_ids)), 1)
        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'name': 'Demo Document For Subcategory 2'})
        self.category_subcat_1.write({
            'owner_user_ids': [(3, self.demo_user.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        # Test owner subategory 2
        self.assertEqual(len(self.category_subcat_2.owner_user_ids), 0)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_user_ids)), 0)

        self.category_subcat_2.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_subcat_2.owner_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_user_ids)), 1)
        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'name': 'Demo Document For Subcategory 2'})
        self.category_subcat_2.write({
            'owner_user_ids': [(3, self.demo_user.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

    def test_document_subcategory_2_restricted_owners_access_write_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')
        self.assertFalse(
            (self.document_subcat_2.actual_visibility_category_id.
             owner_group_ids))
        self.assertEqual(
            len(self.document_subcat_2.actual_visibility_category_id.
                owner_user_ids), 0)
        self.assertFalse(self.document_subcat_2.owner_group_ids)
        self.assertEqual(len(self.document_subcat_2.owner_user_ids), 0)
        self.assertFalse(self.document_subcat_2.actual_owner_group_ids)
        self.assertEqual(len(self.document_subcat_2.actual_owner_user_ids), 0)

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        # Add owner group to Top level category
        self.category_top_level.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.owner_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_group_ids)), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).name,
            'Demo Document For Subcategory 2')

        self.category_top_level.write({
            'owner_group_ids': [(3, self.group_demo.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        # Test owner group subategory 1
        self.assertFalse(self.category_subcat_1.owner_group_ids)
        self.assertFalse(self.document_subcat_2.actual_owner_group_ids)

        self.category_subcat_1.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_subcat_1.owner_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_group_ids)), 1)
        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'name': 'Demo Document For Subcategory 2'})
        self.category_subcat_1.write({
            'owner_group_ids': [(3, self.group_demo.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})

        # Test owner group subategory 2
        self.assertFalse(self.category_subcat_1.owner_group_ids)
        self.assertFalse(self.document_subcat_2.actual_owner_group_ids)

        self.category_subcat_2.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_subcat_2.owner_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_group_ids)), 1)
        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

        self.document_subcat_2.write({
            'name': 'Demo Document For Subcategory 2'})

        self.category_subcat_2.write({
            'owner_group_ids': [(3, self.group_demo.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).write({
                'name': 'Demo Document For Subcategory 2 renamed'})
