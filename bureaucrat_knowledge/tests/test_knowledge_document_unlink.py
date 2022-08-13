from odoo.exceptions import AccessError
from .test_common import TestBureaucratKnowledgeBase


class TestKnowledgeDocumentUnlink(TestBureaucratKnowledgeBase):

    @classmethod
    def setUpClass(cls):
        super(TestKnowledgeDocumentUnlink, cls).setUpClass()
        cls.demo_user.groups_id |= cls.group_knowledge_user

    # Testing document
    def test_document_restricted_access_unlink_user(self):
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
            self.document_subcat_2.with_user(self.demo_user).unlink()

    def test_document_restricted_access_unlink_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertFalse(self.document_subcat_2.visibility_group_ids)
        self.assertFalse(self.document_subcat_2.visibility_user_ids)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.document_subcat_2.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

    def test_document_restricted_editors_access_unlink_user(self):
        self.assertFalse(self.document_subcat_2.editor_group_ids)
        self.assertFalse(self.document_subcat_2.editor_user_ids)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.document_subcat_2.editor_user_ids), 1)

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

    def test_document_restricted_editors_access_unlink_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertFalse(self.document_subcat_2.editor_group_ids)
        self.assertFalse(self.document_subcat_2.editor_user_ids)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.document_subcat_2.editor_group_ids), 1)

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

    def test_document_restricted_owners_access_unlink_user(self):
        Document = self.env['bureaucrat.knowledge.document']
        document = Document.create({
            'document_format': 'html',
            'name': 'Test document',
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id
        })

        self.assertFalse(document.owner_group_ids)
        self.assertEqual(len(document.owner_user_ids), 0)

        document.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            document.with_user(self.demo_user).unlink()

        document.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(document.owner_user_ids), 1)
        document.with_user(self.demo_user).unlink()

    def test_document_restricted_owners_access_unlink_group(self):
        self.demo_user.groups_id |= self.group_demo

        Document = self.env['bureaucrat.knowledge.document']
        document = Document.create({
            'document_format': 'html',
            'name': 'Test document',
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id
        })

        self.assertFalse(document.owner_group_ids)
        self.assertEqual(len(document.owner_user_ids), 0)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(AccessError):
            document.with_user(self.demo_user).unlink()

        document.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(document.owner_group_ids), 1)
        document.with_user(self.demo_user).unlink()

    # Testing document visibility_type = 'public'
    def test_document_public_access_unlink_user(self):
        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

    # Testing document visibility_type = 'public' from parent category
    def test_parent_document_public_access_unlink_user(self):
        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

    # Testing document visibility_type = 'portal'
    def test_document_portal_access_unlink_user(self):
        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

    # Testing document visibility_type = 'portal' from parent category
    def test_parent_document_portal_access_unlink_user(self):
        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.portal_user).unlink()

        self.category_top_level.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.portal_user).unlink()

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.portal_user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.portal_user).unlink()

        self.document_subcat_2.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.portal_user).unlink()

    # Testing document visibility_type = 'internal'
    def test_document_internal_access_unlink_user(self):
        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

    # Testing document visibility_type = 'internal' from parent category
    def test_parent_document_internal_access_unlink_user(self):
        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'restricted'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.document_subcat_2.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

    # Testing document with categoy, for visibility_type = 'restricted'
    def test_document_subcategory_2_restricted_access_unlink_user(self):
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
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_visibility_category_id.
                 visibility_user_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

    def test_document_subcategory_2_restricted_access_unlink_group(self):
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
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_visibility_category_id.
                 visibility_group_ids)), 1)

        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

    def test_document_subcategory_2_restricted_editors_access_unlink_user(
            self):
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
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.editor_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_user_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.write({
            'editor_user_ids': [(3, self.demo_user.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        # Test editor subategory 1
        self.assertFalse(self.category_subcat_1.editor_user_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_user_ids)

        self.category_subcat_1.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_subcat_1.editor_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_user_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.category_subcat_1.write({
            'editor_user_ids': [(3, self.demo_user.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        # Test editor subategory 2
        self.assertFalse(self.category_subcat_1.editor_user_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_user_ids)

        self.category_subcat_2.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_subcat_2.editor_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_user_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.category_subcat_2.write({
            'editor_user_ids': [(3, self.demo_user.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

    def test_document_subcategory_2_restricted_editors_access_unlink_group(
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
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.editor_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_visibility_category_id.
                 editor_group_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.write({
            'editor_group_ids': [(3, self.group_demo.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        # Test editor subategory 1
        self.assertFalse(self.category_subcat_1.editor_group_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_group_ids)

        self.category_subcat_1.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_subcat_1.editor_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_group_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()
        self.document_subcat_2.with_user(self.demo_user).write({
            'name': 'Demo Document For Subcategory 2 renamed'})

        self.category_subcat_1.write({
            'editor_group_ids': [(3, self.group_demo.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        # Test editor subategory 2
        self.assertFalse(self.category_subcat_2.editor_group_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_group_ids)

        self.category_subcat_2.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_subcat_2.editor_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_group_ids)), 1)
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        self.category_subcat_2.write({
            'editor_group_ids': [(3, self.group_demo.id)]})
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

    def test_document_subcategory_2_restricted_owners_access_unlink_user(self):
        Document = self.env['bureaucrat.knowledge.document']
        document_subcat_2 = Document.create({
            'name': 'Test document',
            'document_format': 'html',
            'category_id': self.category_subcat_2.id,
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id
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
                owner_user_ids), 0)
        self.assertFalse(document_subcat_2.owner_group_ids)
        self.assertEqual(len(document_subcat_2.owner_user_ids), 0)
        self.assertFalse(document_subcat_2.actual_owner_group_ids)
        self.assertEqual(len(document_subcat_2.actual_owner_user_ids), 0)

        with self.assertRaises(AccessError):
            document_subcat_2.with_user(self.demo_user).unlink()

        # Add owner to Top level category
        self.category_top_level.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.owner_user_ids), 1)
        self.assertEqual(
            len((document_subcat_2.actual_owner_user_ids)), 1)
        document_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.write({
            'owner_user_ids': [(3, self.demo_user.id)]})

        document_subcat_2 = Document.create({
            'name': 'Test document',
            'document_format': 'html',
            'category_id': self.category_subcat_2.id,
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id
        })
        with self.assertRaises(AccessError):
            self.document_subcat_2.with_user(self.demo_user).unlink()

        # Test owner subategory 1
        self.assertEqual(len(self.category_subcat_1.owner_user_ids), 0)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_user_ids)), 0)

        self.category_subcat_1.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_subcat_1.owner_user_ids), 1)
        self.assertEqual(
            len((document_subcat_2.actual_owner_user_ids)), 1)
        document_subcat_2.with_user(self.demo_user).unlink()

        self.category_subcat_1.write({
            'owner_user_ids': [(3, self.demo_user.id)]})

        document_subcat_2 = Document.create({
            'name': 'Test document',
            'document_format': 'html',
            'category_id': self.category_subcat_2.id,
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id
        })
        with self.assertRaises(AccessError):
            document_subcat_2.with_user(self.demo_user).unlink()

        # Test owner subategory 2
        self.assertEqual(len(self.category_subcat_2.owner_user_ids), 0)
        self.assertEqual(
            len((document_subcat_2.actual_owner_user_ids)), 0)

        self.category_subcat_2.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_subcat_2.owner_user_ids), 1)
        self.assertEqual(
            len((document_subcat_2.actual_owner_user_ids)), 1)
        document_subcat_2.with_user(self.demo_user).unlink()

        self.category_subcat_2.write({
            'owner_user_ids': [(3, self.demo_user.id)]})

        document_subcat_2 = Document.create({
            'name': 'Test document',
            'document_format': 'html',
            'category_id': self.category_subcat_2.id,
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id
        })
        with self.assertRaises(AccessError):
            document_subcat_2.with_user(self.demo_user).unlink()

    def test_document_subcategory_2_restricted_owners_access_unlink_group(
            self):
        self.demo_user.groups_id |= self.group_demo

        # TODO: find out why self.group_demo.id
        # not assigned to category_subcat_2.actual_owner_group_ids
        # when category created in this method

        Document = self.env['bureaucrat.knowledge.document']
        document_subcat_2 = Document.create({
            'name': 'Test document',
            'document_format': 'html',
            'category_id': self.category_subcat_2.id,
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id
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
                owner_user_ids), 0)
        self.assertFalse(document_subcat_2.owner_group_ids)
        self.assertEqual(len(document_subcat_2.owner_user_ids), 0)
        self.assertFalse(document_subcat_2.actual_owner_group_ids)
        self.assertEqual(len(document_subcat_2.actual_owner_user_ids), 0)

        with self.assertRaises(AccessError):
            document_subcat_2.with_user(self.demo_user).unlink()

        # Add owner group to Top level category
        self.category_top_level.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.owner_group_ids), 1)
        self.assertEqual(
            len((document_subcat_2.actual_owner_group_ids)), 1)
        document_subcat_2.with_user(self.demo_user).unlink()

        self.category_top_level.write({
            'owner_group_ids': [(3, self.group_demo.id)]})

        document_subcat_2 = Document.create({
            'name': 'Test document',
            'document_format': 'html',
            'category_id': self.category_subcat_2.id,
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id
        })
        with self.assertRaises(AccessError):
            document_subcat_2.with_user(self.demo_user).unlink()

        # Test owner group subategory 1
        self.assertFalse(self.category_subcat_1.owner_group_ids)
        self.assertFalse(document_subcat_2.actual_owner_group_ids)

        self.category_subcat_1.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_subcat_1.owner_group_ids), 1)
        self.assertEqual(
            len((document_subcat_2.actual_owner_group_ids)), 1)
        document_subcat_2.with_user(self.demo_user).unlink()

        self.category_subcat_1.write({
            'owner_group_ids': [(3, self.group_demo.id)]})

        document_subcat_2 = Document.create({
            'name': 'Test document',
            'document_format': 'html',
            'category_id': self.category_subcat_2.id,
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id
        })
        with self.assertRaises(AccessError):
            document_subcat_2.with_user(self.demo_user).unlink()

        # Test owner group subategory 2
        self.assertFalse(self.category_subcat_1.owner_group_ids)
        self.assertFalse(document_subcat_2.actual_owner_group_ids)

        self.category_subcat_2.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_subcat_2.owner_group_ids), 1)
        self.assertEqual(
            len((document_subcat_2.actual_owner_group_ids)), 1)
        document_subcat_2.with_user(self.demo_user).unlink()

        self.category_subcat_2.write({
            'owner_group_ids': [(3, self.group_demo.id)]})

        document_subcat_2 = Document.create({
            'name': 'Test document',
            'document_format': 'html',
            'category_id': self.category_subcat_2.id,
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id
        })
        with self.assertRaises(AccessError):
            document_subcat_2.with_user(self.demo_user).unlink()
