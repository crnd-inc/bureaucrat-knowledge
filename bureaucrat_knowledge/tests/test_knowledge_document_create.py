from odoo.exceptions import AccessError
from .test_common import TestBureaucratKnowledgeBase


class TestKnowledgeDocumentCreate(TestBureaucratKnowledgeBase):

    @classmethod
    def setUpClass(cls):
        super(TestKnowledgeDocumentCreate, cls).setUpClass()
        cls.demo_user.groups_id |= cls.group_knowledge_user

    # Testing Top level document for visibility_type = 'restricted'
    def test_document_restricted_access_create_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

    def test_document_restricted_access_create_user2(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'editor_user_ids': [(4, self.demo_user.id)]})

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'editor_user_ids': [(4, self.demo_user.id)]})

    def test_document_restricted_access_create_user3(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'owner_user_ids': [(4, self.demo_user.id)]})

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'owner_user_ids': [(4, self.demo_user.id)]})

    def test_document_restricted_access_create_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

    def test_document_restricted_access_create_group2(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'editor_group_ids': [(4, self.group_demo.id)]})

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'editor_group_ids': [(4, self.group_demo.id)]})

    def test_document_restricted_access_create_group3(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'owner_group_ids': [(4, self.group_demo.id)]})

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'owner_group_ids': [(4, self.group_demo.id)]})

    def test_document_restricted_editors_access_create_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)

        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.editor_user_ids), 1)
        document = self.Document.with_user(self.demo_user).create({
            'name': 'Test Create',
            'document_type': 'html',
            'category_id': self.category_top_level.id,
            'document_body_html': 'Test Document'})
        self.assertEqual(document.visibility_type, 'parent')
        self.assertFalse(document.visibility_user_ids)
        self.assertFalse(document.visibility_group_ids)
        self.assertFalse(document.editor_group_ids)
        self.assertFalse(document.editor_user_ids)
        self.assertFalse(document.owner_group_ids)
        self.assertFalse(document.owner_user_ids)

    def test_document_restricted_editors_access_create_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)

        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.editor_group_ids), 1)
        document = self.Document.with_user(self.demo_user).create({
            'name': 'Test Create',
            'document_type': 'html',
            'category_id': self.category_top_level.id,
            'document_body_html': 'Test Document'})
        self.assertEqual(document.visibility_type, 'parent')
        self.assertFalse(document.visibility_user_ids)
        self.assertFalse(document.visibility_group_ids)
        self.assertFalse(document.editor_group_ids)
        self.assertFalse(document.editor_user_ids)
        self.assertFalse(document.owner_group_ids)
        self.assertFalse(document.owner_user_ids)

    def test_document_restricted_owners_access_create_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.owner_group_ids)
        self.assertEqual(len(self.category_top_level.owner_user_ids), 0)

        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.owner_user_ids), 1)
        document = self.Document.with_user(self.demo_user).create({
            'name': 'Test Create',
            'document_type': 'html',
            'category_id': self.category_top_level.id,
            'document_body_html': 'Test Document'})
        self.assertEqual(document.visibility_type, 'parent')
        self.assertFalse(document.visibility_user_ids)
        self.assertFalse(document.visibility_group_ids)
        self.assertFalse(document.editor_group_ids)
        self.assertFalse(document.editor_user_ids)
        self.assertFalse(document.owner_group_ids)
        self.assertFalse(document.owner_user_ids)

    def test_document_restricted_owners_access_create_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.owner_group_ids)
        self.assertEqual(len(self.category_top_level.owner_user_ids), 0)

        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.owner_group_ids), 1)
        document = self.Document.with_user(self.demo_user).create({
            'name': 'Test Create',
            'document_type': 'html',
            'category_id': self.category_top_level.id,
            'document_body_html': 'Test Document'})
        self.assertEqual(document.visibility_type, 'parent')
        self.assertFalse(document.visibility_user_ids)
        self.assertFalse(document.visibility_group_ids)
        self.assertFalse(document.editor_group_ids)
        self.assertFalse(document.editor_user_ids)
        self.assertFalse(document.owner_group_ids)
        self.assertFalse(document.owner_user_ids)

    def test_document_create_top_level(self):
        document = self.Document.with_user(self.demo_user).create({
            'name': 'Test Create',
            'document_type': 'html',
            'document_body_html': 'Test Document'})
        self.assertEqual(document.visibility_type, 'restricted')
        self.assertFalse(document.visibility_user_ids)
        self.assertFalse(document.visibility_group_ids)
        self.assertFalse(document.editor_group_ids)
        self.assertFalse(document.editor_user_ids)
        self.assertFalse(document.owner_group_ids)
        self.assertIn(self.demo_user, document.owner_user_ids)

    # Testing Top level document for visibility_type = 'public'
    def test_document_public_access_create_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')

        with self.assertRaises(AccessError):
            self.Document.with_user(self.public_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.Document.with_user(self.public_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.Document.with_user(self.public_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'public'

        with self.assertRaises(AccessError):
            self.Document.with_user(self.public_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

    # Testing Top level category for visibility_type = 'portal'
    def test_document_portal_access_create_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')

        with self.assertRaises(AccessError):
            self.Document.with_user(self.portal_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.Document.with_user(self.portal_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.Document.with_user(self.portal_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.Document.with_user(self.portal_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

    # Testing Top level document for visibility_type = 'internal'
    def test_document_internal_access_create_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')

        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'internal'

        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create',
                'document_type': 'html',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document'})

    # Testing subcategory 2nd level depth for visibility_type = 'restricted'
    def test_subcategory_2_restricted_access_create_user(self):
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
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

    def test_subdocument_2_restricted_access_create_group(self):
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
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

    def test_subdocument_2_restricted_editors_access_create_user(self):
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
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

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

        document = self.Document.with_user(self.demo_user).create({
            'name': 'Test Create Sub 1',
            'document_type': 'html',
            'category_id': self.category_subcat_2.id,
            'document_body_html': 'Test Document'})
        self.assertEqual(document.visibility_type, 'parent')
        self.assertFalse(document.visibility_user_ids)
        self.assertFalse(document.visibility_group_ids)
        self.assertFalse(document.editor_group_ids)
        self.assertFalse(document.editor_user_ids)
        self.assertFalse(document.owner_group_ids)
        self.assertFalse(document.owner_user_ids)

    def test_subdocument_2_restricted_editors_access_create_group(self):
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
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

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

        document = self.Document.with_user(self.demo_user).create({
            'name': 'Test Create Sub 1',
            'document_type': 'html',
            'category_id': self.category_subcat_2.id,
            'document_body_html': 'Test Document'})
        self.assertEqual(document.visibility_type, 'parent')
        self.assertFalse(document.visibility_user_ids)
        self.assertFalse(document.visibility_group_ids)
        self.assertFalse(document.editor_group_ids)
        self.assertFalse(document.editor_user_ids)
        self.assertFalse(document.owner_group_ids)
        self.assertFalse(document.owner_user_ids)

    def test_subdocument2_restricted_owners_access_create_user(self):
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
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

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

        document = self.Document.with_user(self.demo_user).create({
            'name': 'Test Create Sub 1',
            'document_type': 'html',
            'category_id': self.category_subcat_2.id,
            'document_body_html': 'Test Document'})
        self.assertEqual(document.visibility_type, 'parent')
        self.assertFalse(document.visibility_user_ids)
        self.assertFalse(document.visibility_group_ids)
        self.assertFalse(document.editor_group_ids)
        self.assertFalse(document.editor_user_ids)
        self.assertFalse(document.owner_group_ids)
        self.assertFalse(document.owner_user_ids)

    def test_subdocument_2_restricted_owners_access_create_group(self):
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
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

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

        document = self.Document.with_user(self.demo_user).create({
            'name': 'Test Create Sub 1',
            'document_type': 'html',
            'category_id': self.category_subcat_2.id,
            'document_body_html': 'Test Document'})
        self.assertEqual(document.visibility_type, 'parent')
        self.assertFalse(document.visibility_user_ids)
        self.assertFalse(document.visibility_group_ids)
        self.assertFalse(document.editor_group_ids)
        self.assertFalse(document.editor_user_ids)
        self.assertFalse(document.owner_group_ids)
        self.assertFalse(document.owner_user_ids)

    # Testing subdocument 2nd level depth for visibility_type = 'public'
    def test_subdocument_public_access_create_user(self):
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
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'public'

        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

    # Testing subdocument 2nd level depth for visibility_type = 'portal'
    def test_subdocument_2_portal_access_create_user(self):
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
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'portal'

        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

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
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.Document.with_user(self.demo_user).create({
                'name': 'Test Create Sub 1',
                'document_type': 'html',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document'})
