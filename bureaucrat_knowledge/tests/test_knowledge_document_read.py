from odoo import exceptions
from .test_common import TestBureaucratKnowledgeBase


class TestKnowledgeDocumentRead(TestBureaucratKnowledgeBase):

    # Testing document
    def test_document_restricted_access_read_user(self):
        self.assertFalse(self.document_subcat_2.visibility_group_ids)
        self.assertFalse(self.document_subcat_2.visibility_user_ids)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        self.document_subcat_2.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.document_subcat_2.visibility_user_ids), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

    def test_document_restricted_access_read_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertFalse(self.document_subcat_2.visibility_group_ids)
        self.assertFalse(self.document_subcat_2.visibility_user_ids)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        self.document_subcat_2.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.document_subcat_2.visibility_group_ids), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

    def test_document_restricted_editors_access_read_user(self):
        self.assertFalse(self.document_subcat_2.editor_group_ids)
        self.assertFalse(self.document_subcat_2.editor_user_ids)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        self.document_subcat_2.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.document_subcat_2.editor_user_ids), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

    def test_document_restricted_editors_access_read_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertFalse(self.document_subcat_2.editor_group_ids)
        self.assertFalse(self.document_subcat_2.editor_user_ids)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        self.document_subcat_2.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.document_subcat_2.editor_group_ids), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

    def test_document_restricted_owners_access_read_user(self):
        self.assertFalse(self.document_subcat_2.owner_group_ids)
        self.assertEqual(len(self.document_subcat_2.owner_user_ids), 0)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        self.document_subcat_2.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.document_subcat_2.owner_user_ids), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

    def test_document_restricted_owners_access_read_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertFalse(self.document_subcat_2.owner_group_ids)
        self.assertEqual(len(self.document_subcat_2.owner_user_ids), 0)

        self.document_subcat_2.visibility_type = 'restricted'

        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        self.document_subcat_2.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.document_subcat_2.owner_group_ids), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).name,
            'Demo Document For Subcategory 2')

    def test_document_public_access_portal_internal_read_user(self):
        # initiall document has visibility type parent
        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        # Set document's visibility type to 'restricted'
        self.document_subcat_2.visibility_type = 'restricted'

        # Ensure nobody can access it
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.portal_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.public_user).read(['name'])

        # Make document internal
        self.document_subcat_2.visibility_type = 'internal'
        self.env['bureaucrat.knowledge.document'].flush_model()

        # Ensure that employees could access this document
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.portal_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.public_user).read(['name'])

        # Make document accessible via portal
        self.document_subcat_2.visibility_type = 'portal'
        self.env['bureaucrat.knowledge.document'].flush_model()

        # Ensure that employees and portal users could access this documnet
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')
        self.assertEqual(
            self.document_subcat_2.with_user(self.portal_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.public_user).read(['name'])

        # Make document public
        self.document_subcat_2.visibility_type = 'public'
        self.env['bureaucrat.knowledge.document'].flush_model()

        # Ensure that even public users could read this document
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')
        self.assertEqual(
            self.document_subcat_2.with_user(self.portal_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')
        self.assertEqual(
            self.document_subcat_2.with_user(self.public_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

    def test_parent_document_public_portal_internal_access_read_user(self):
        self.assertEqual(
            self.document_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.document_subcat_2.actual_visibility_category_id.
             visibility_type), 'restricted')

        # Nobody can access document from restricted category
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.portal_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.public_user).read(['name'])

        # Change visibility to internal
        self.category_top_level.visibility_type = 'internal'

        # And check that employees could see this category
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.public_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.portal_user).read(['name'])

        # Change visibility to portal
        self.category_top_level.visibility_type = 'portal'

        # And check that employees and portal users could see this category
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')
        self.assertEqual(
            self.document_subcat_2.with_user(self.portal_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.public_user).read(['name'])

        # Change visibility to public
        self.category_top_level.visibility_type = 'public'

        # And check that employees, portal and public users could see
        # this category
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')
        self.assertEqual(
            self.document_subcat_2.with_user(self.portal_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')
        self.assertEqual(
            self.document_subcat_2.with_user(self.public_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

        # Change visibility time of subcategory level 1 to 'internal'
        self.category_subcat_1.visibility_type = 'internal'
        self.env['bureaucrat.knowledge.document'].flush_model()

        # And check that only employees can see subcategory (level 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.portal_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.public_user).read(['name'])

        # Change visibility type to 'restricted' for subcategory level 2
        self.document_subcat_2.visibility_type = 'portal'
        self.env['bureaucrat.knowledge.document'].flush_model()

        # And check that nobody can see subcategory (level 2)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')
        self.assertEqual(
            self.document_subcat_2.with_user(self.portal_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.public_user).read(['name'])

    # Testing document with categoy, for categ visibility_type = 'restricted'
    def test_document_subcategory_2_restricted_access_read_user(self):
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

        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_visibility_category_id.
                 visibility_user_ids)), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

    def test_document_subcategory_2_restricted_access_read_group(self):
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

        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_visibility_category_id.
                 visibility_group_ids)), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

    def test_document_subcategory_2_restricted_editors_access_read_user(self):
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

        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        self.category_top_level.write({
            'editor_user_ids': [(4, self.demo_user.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()

        self.assertEqual(len(self.category_top_level.editor_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_user_ids)), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

        self.category_top_level.write({
            'editor_user_ids': [(3, self.demo_user.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        # Test editor subategory 1
        self.assertFalse(self.category_subcat_1.editor_user_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_user_ids)

        self.category_subcat_1.write({
            'editor_user_ids': [(4, self.demo_user.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()

        self.assertEqual(len(self.category_subcat_1.editor_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_user_ids)), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

        self.category_subcat_1.write({
            'editor_user_ids': [(3, self.demo_user.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        # Test editor subategory 2
        self.assertFalse(self.category_subcat_1.editor_user_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_user_ids)

        self.category_subcat_2.write({
            'editor_user_ids': [(4, self.demo_user.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()

        self.assertEqual(len(self.category_subcat_2.editor_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_user_ids)), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

        self.category_subcat_2.write({
            'editor_user_ids': [(3, self.demo_user.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

    def test_document_subcategory_2_restricted_editors_access_read_group(self):
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

        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        self.category_top_level.write({
            'editor_group_ids': [(4, self.group_demo.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()

        self.assertEqual(len(self.category_top_level.editor_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_visibility_category_id.
                 editor_group_ids)), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

        self.category_top_level.write({
            'editor_group_ids': [(3, self.group_demo.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        # Test editor subategory 1
        self.assertFalse(self.category_subcat_1.editor_group_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_group_ids)

        self.category_subcat_1.write({
            'editor_group_ids': [(4, self.group_demo.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()

        self.assertEqual(len(self.category_subcat_1.editor_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_group_ids)), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

        self.category_subcat_1.write({
            'editor_group_ids': [(3, self.group_demo.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        # Test owner subategory 2
        self.assertFalse(self.category_subcat_2.editor_group_ids)
        self.assertFalse(self.document_subcat_2.actual_editor_group_ids)

        self.category_subcat_2.write({
            'editor_group_ids': [(4, self.group_demo.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()

        self.assertEqual(len(self.category_subcat_2.editor_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_editor_group_ids)), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

        self.category_subcat_2.write({
            'editor_group_ids': [(3, self.group_demo.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

    def test_document_subcategory_2_restricted_owners_access_read_user(self):
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

        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        # Add owner to Top level category
        self.category_top_level.write({
            'owner_user_ids': [(4, self.demo_user.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()

        self.assertEqual(len(self.category_top_level.owner_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_user_ids)), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

        self.category_top_level.write({
            'owner_user_ids': [(3, self.demo_user.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        # Test owner subategory 1
        self.assertEqual(len(self.category_subcat_1.owner_user_ids), 0)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_user_ids)), 0)

        self.category_subcat_1.write({
            'owner_user_ids': [(4, self.demo_user.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()

        self.assertEqual(len(self.category_subcat_1.owner_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_user_ids)), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

        self.category_subcat_1.write({
            'owner_user_ids': [(3, self.demo_user.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        # Test owner subategory 2
        self.assertEqual(len(self.category_subcat_2.owner_user_ids), 0)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_user_ids)), 0)

        self.category_subcat_2.write({
            'owner_user_ids': [(4, self.demo_user.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()

        self.assertEqual(len(self.category_subcat_2.owner_user_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_user_ids)), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

        self.category_subcat_2.write({
            'owner_user_ids': [(3, self.demo_user.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

    def test_document_subcategory_2_restricted_owners_access_read_group(self):
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

        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        # Add owner group to Top level category
        self.category_top_level.write({
            'owner_group_ids': [(4, self.group_demo.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()

        self.assertEqual(len(self.category_top_level.owner_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_group_ids)), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

        self.category_top_level.write({
            'owner_group_ids': [(3, self.group_demo.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        # Test owner group subategory 1
        self.assertFalse(self.category_subcat_1.owner_group_ids)
        self.assertFalse(self.document_subcat_2.actual_owner_group_ids)

        self.category_subcat_1.write({
            'owner_group_ids': [(4, self.group_demo.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()

        self.assertEqual(len(self.category_subcat_1.owner_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_group_ids)), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

        self.category_subcat_1.write({
            'owner_group_ids': [(3, self.group_demo.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])

        # Test owner group subategory 2
        self.assertFalse(self.category_subcat_1.owner_group_ids)
        self.assertFalse(self.document_subcat_2.actual_owner_group_ids)

        self.category_subcat_2.write({
            'owner_group_ids': [(4, self.group_demo.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()

        self.assertEqual(len(self.category_subcat_2.owner_group_ids), 1)
        self.assertEqual(
            len((self.document_subcat_2.actual_owner_group_ids)), 1)
        self.assertEqual(
            self.document_subcat_2.with_user(self.demo_user).read(
                ['name'])[0]['name'],
            'Demo Document For Subcategory 2')

        self.category_subcat_2.write({
            'owner_group_ids': [(3, self.group_demo.id)]})
        self.env['bureaucrat.knowledge.document'].flush_model()
        with self.assertRaises(exceptions.AccessError):
            self.document_subcat_2.with_user(self.demo_user).read(['name'])
