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
            self.Document.sudo(self.demo_user).create({
                'name': 'Test Create 1',
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '335'})

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create1',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '336'})

    def test_document_restricted_access_create_user2(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create2',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'editor_user_ids': [(4, self.demo_user.id)],
                'code': '339'
                })

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create3',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'editor_user_ids': [(4, self.demo_user.id)],
                'code': '337',
            })

    def test_document_restricted_access_create_user3(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create4',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'owner_user_ids': [(4, self.demo_user.id)],
                'code': '340'})

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create5',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'owner_user_ids': [(4, self.demo_user.id)],
                'code': '341'})

    def test_document_restricted_access_create_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create6',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '342'})

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create7',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '343'})

    def test_document_restricted_access_create_group2(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create8',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'editor_group_ids': [(4, self.group_demo.id)],
                'code': '344'})

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create9',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'editor_group_ids': [(4, self.group_demo.id)],
                'code': '345'})

    def test_document_restricted_access_create_group3(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create10',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'owner_group_ids': [(4, self.group_demo.id)],
                'code': '346'})

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create11',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'owner_group_ids': [(4, self.group_demo.id)],
                'code': '347'})

    def test_document_restricted_editors_access_create_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)

        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create12',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '348'})

        self.category_top_level.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.editor_user_ids), 1)
        document = self.Document.sudo(self.demo_user).create({
            'document_format': 'html',
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id,
            'name': 'Test Create13',
            'category_id': self.category_top_level.id,
            'document_body_html': 'Test Document',
            'code': '349'})
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
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create14',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '350'})

        self.category_top_level.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.editor_group_ids), 1)
        document = self.Document.sudo(self.demo_user).create({
            'document_format': 'html',
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id,
            'name': 'Test Create15',
            'category_id': self.category_top_level.id,
            'document_body_html': 'Test Document',
            'code': '351'})
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
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create16',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '352'})

        self.category_top_level.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.owner_user_ids), 1)
        document = self.Document.sudo(self.demo_user).create({
            'document_format': 'html',
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id,
            'name': 'Test Create161',
            'category_id': self.category_top_level.id,
            'document_body_html': 'Test Document',
            'code': '353'})
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
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create17',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '354'})

        self.category_top_level.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.owner_group_ids), 1)
        document = self.Document.sudo(self.demo_user).create({
            'document_format': 'html',
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id,
            'name': 'Test Create18',
            'category_id': self.category_top_level.id,
            'document_body_html': 'Test Document',
            'code': '355'})
        self.assertEqual(document.visibility_type, 'parent')
        self.assertFalse(document.visibility_user_ids)
        self.assertFalse(document.visibility_group_ids)
        self.assertFalse(document.editor_group_ids)
        self.assertFalse(document.editor_user_ids)
        self.assertFalse(document.owner_group_ids)
        self.assertFalse(document.owner_user_ids)

    def test_document_create_top_level(self):
        document = self.Document.sudo(self.demo_user).create({
            'document_format': 'html',
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id,
            'name': 'Test Create19',
            'document_body_html': 'Test Document',
            'code': '356'})
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
            self.Document.sudo(self.public_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create20',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '357'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.Document.sudo(self.public_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create21',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '358'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.Document.sudo(self.public_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create22',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '359'})

        self.category_top_level.visibility_type = 'public'

        with self.assertRaises(AccessError):
            self.Document.sudo(self.public_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create23',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '360'})

    # Testing Top level category for visibility_type = 'portal'
    def test_document_portal_access_create_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')

        with self.assertRaises(AccessError):
            self.Document.sudo(self.portal_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create24',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '361'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.Document.sudo(self.portal_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create25',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '362'})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.Document.sudo(self.portal_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create26',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '363'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.Document.sudo(self.portal_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create27',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '364'})

    # Testing Top level document for visibility_type = 'internal'
    def test_document_internal_access_create_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')

        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create28',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '365'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create29',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '366'})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create30',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '367'})

        self.category_top_level.visibility_type = 'internal'

        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create31',
                'category_id': self.category_top_level.id,
                'document_body_html': 'Test Document',
                'code': '368'})

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
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create Sub 9',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '369'})

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create Sub 10',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '370'})

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
            self.Document.sudo(self.demo_user).create({
                'name': 'Test Create Sub 12',
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '380'})

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'name': 'Test Create Sub 13',
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '381'})

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
            self.Document.sudo(self.demo_user).create({
                'name': 'Test Create Sub 14',
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '382'})

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

        document = self.Document.sudo(self.demo_user).create({
            'name': 'Test Create Sub 15',
            'document_format': 'html',
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id,
            'category_id': self.category_subcat_2.id,
            'document_body_html': 'Test Document',
            'code': '383'})
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
            self.Document.sudo(self.demo_user).create({
                'name': 'Test Create Sub 16',
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '384'})

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

        document = self.Document.sudo(self.demo_user).create({
            'name': 'Test Create Sub 17',
            'document_format': 'html',
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id,
            'category_id': self.category_subcat_2.id,
            'document_body_html': 'Test Document',
            'code': '385'})
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
            self.Document.sudo(self.demo_user).create({
                'name': 'Test Create Sub 18',
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '386'})

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

        document = self.Document.sudo(self.demo_user).create({
            'name': 'Test Create Sub 19',
            'document_format': 'html',
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id,
            'category_id': self.category_subcat_2.id,
            'document_body_html': 'Test Document',
            'code': '387'})
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
            self.Document.sudo(self.demo_user).create({
                'name': 'Test Create Sub 20',
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '388'})

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

        document = self.Document.sudo(self.demo_user).create({
            'name': 'Test Create Sub 21',
            'document_format': 'html',
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id,
            'category_id': self.category_subcat_2.id,
            'document_body_html': 'Test Document',
            'code': '390'})
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
            self.Document.sudo(self.demo_user).create({
                'name': 'Test Create Sub 22',
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '391'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'name': 'Test Create Sub 23',
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '392'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'name': 'Test Create Sub 24',
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '393'})

        self.category_top_level.visibility_type = 'public'

        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'name': 'Test Create Sub 25',
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '394'})

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
            self.Document.sudo(self.demo_user).create({
                'name': 'Test Create Sub 26',
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '395'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'name': 'Test Create Sub 27',
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '396'})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'name': 'Test Create Sub 28',
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '397'})

        self.category_top_level.visibility_type = 'portal'

        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'name': 'Test Create Sub 29',
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '398'})

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
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create Sub 31',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '399'})

        self.category_top_level.visibility_type = 'portal'
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create Sub 32',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '400'})

        self.category_top_level.visibility_type = 'public'
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create Sub 33',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '401'})

        self.category_top_level.visibility_type = 'internal'
        with self.assertRaises(AccessError):
            self.Document.sudo(self.demo_user).create({
                'document_format': 'html',
                'document_type_id': self.env.ref(
                    'bureaucrat_knowledge.bureaucrat_document_type_art').id,
                'name': 'Test Create Sub 34',
                'category_id': self.category_subcat_2.id,
                'document_body_html': 'Test Document',
                'code': '402'})
