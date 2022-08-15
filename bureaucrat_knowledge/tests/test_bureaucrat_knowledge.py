import logging
from .test_common import TestBureaucratKnowledgeBase

_logger = logging.getLogger(__name__)


class TestBureaucratKnowledge(TestBureaucratKnowledgeBase):

    def test_category_default_values(self):
        self.demo_user.groups_id |= self.env.ref(
            'bureaucrat_knowledge.group_bureaucratic_knowledge_user')

        Category = self.env['bureaucrat.knowledge.category']
        category = Category.with_user(self.demo_user).create({
            'name': 'Test top level category',
            'code': 'test-top',
        })

        self.assertEqual(category.visibility_type, 'restricted')
        self.assertEqual(len(category.owner_user_ids), 1)
        self.assertIn(self.demo_user, category.owner_user_ids)
        self.assertFalse(category.editor_user_ids)

        category.write({
            'editor_user_ids': [(6, 0, [self.demo_user.id])]})

        subcategory = Category.with_user(self.demo_user).create({
            'name': 'Test subcategory',
            'parent_id': category.id,
            'code': 'test-cat',
        })

        # Without this test does not pass. It seems that parent left/right are
        # not recomputed just after write
        self.env['bureaucrat.knowledge.category']._parent_store_compute()

        self.assertEqual(len(category.editor_user_ids), 1)
        self.assertEqual(len(category.actual_editor_user_ids), 1)
        self.assertIn(self.demo_user, category.editor_user_ids)
        self.assertIn(self.demo_user, category.actual_editor_user_ids)
        self.assertEqual(subcategory.visibility_type, 'parent')
        self.assertEqual(len(subcategory.owner_user_ids), 0)

        self.assertFalse(subcategory.editor_user_ids)
        self.assertEqual(len(subcategory.actual_editor_user_ids), 1)
        self.assertIn(self.demo_user, subcategory.actual_editor_user_ids)

        subcategory2 = Category.with_user(self.demo_user).create({
            'name': 'Test subcategory2',
            'parent_id': subcategory.id,
            'code': 'test-cat2',
        })

        # Without this test does not pass. It seems that parent left/right are
        # not recomputed just after write
        self.env['bureaucrat.knowledge.category']._parent_store_compute()

        self.assertEqual(subcategory2.visibility_type, 'parent')
        self.assertEqual(len(subcategory2.owner_user_ids), 0)
        self.assertFalse(subcategory2.editor_user_ids)
        self.assertEqual(len(subcategory2.actual_editor_user_ids), 1)
        self.assertIn(self.demo_user, subcategory2.actual_editor_user_ids)

    def test_document_default_values(self):
        self.demo_user.groups_id |= self.env.ref(
            'bureaucrat_knowledge.group_bureaucratic_knowledge_user')

        Document = self.env['bureaucrat.knowledge.document']
        document = Document.with_user(self.demo_user).create({
            'name': 'Test top level document',
            'document_format': 'html',
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id
        })

        self.assertEqual(document.visibility_type, 'restricted')
        self.assertEqual(len(document.owner_user_ids), 1)
        self.assertIn(self.demo_user, document.owner_user_ids)

        Category = self.env['bureaucrat.knowledge.category']
        category = Category.with_user(self.demo_user).create({
            'name': 'Test top level category2',
            'code': 'top_l2',
            'editor_user_ids': [(4, self.demo_user.id)],
        })

        subdocument = Document.with_user(self.demo_user).create({
            'name': 'Test top level document1',
            'category_id': category.id,
            'document_format': 'html',
            'document_type_id': self.env.ref(
                'bureaucrat_knowledge.bureaucrat_document_type_art').id
        })

        self.assertEqual(subdocument.visibility_type, 'parent')
        self.assertEqual(len(subdocument.owner_user_ids), 0)
        self.assertFalse(subdocument.editor_user_ids)
        self.assertEqual(len(subdocument.actual_editor_user_ids), 1)
        self.assertIn(self.demo_user, subdocument.actual_editor_user_ids)

    def test_document_search_by_index_field(self):
        Document = self.env['bureaucrat.knowledge.document']
        self.assertEqual(self.document_subcat_2_with_pdf.document_type, 'pdf')
        self.assertIn(
            'Lorem Ipsum',
            self.document_subcat_2_with_pdf._get_document_index()
        )
        documents = Document.search([
            ('index_document_body', 'ilike', 'lorem ipsum')])
        self.assertIn(self.document_subcat_2_with_pdf, documents)

    def test_document_code_generation_no_categ_auto_number(self):
        doc_type = self.env.ref(
            'bureaucrat_knowledge.bureaucrat_document_type_rfc')
        doc = self.env['bureaucrat.knowledge.document'].create({
            'name': 'Test document 123543',
            'document_format': 'html',
            'document_type_id': doc_type.id,
            'document_body_html': "<p>Test</p>",
        })

        self.assertRegex(doc.document_number, r'D\d{4}')
        self.assertRegex(doc.code, r'RFC_D\d{4}')

    def test_document_code_generation_no_categ_custom_number(self):
        doc_type = self.env.ref(
            'bureaucrat_knowledge.bureaucrat_document_type_rfc')
        doc = self.env['bureaucrat.knowledge.document'].create({
            'name': 'Test document 123543',
            'document_format': 'html',
            'document_type_id': doc_type.id,
            'document_body_html': "<p>Test</p>",
            'document_number': 'TST13',
        })

        self.assertEqual(doc.document_number, 'TST13')
        self.assertEqual(doc.code, r'RFC_TST13')

    def test_document_code_generation_with_categ_auto_number(self):
        category = self.env['bureaucrat.knowledge.category'].create({
            'name': 'Test Categ 13',
            'code': 'CST18',
        })
        doc_type = self.env.ref(
            'bureaucrat_knowledge.bureaucrat_document_type_rfc')
        doc = self.env['bureaucrat.knowledge.document'].create({
            'name': 'Test document 123543',
            'document_format': 'html',
            'document_type_id': doc_type.id,
            'document_body_html': "<p>Test</p>",
            'category_id': category.id,
        })

        self.assertRegex(doc.document_number, r'D\d{4}')
        self.assertRegex(doc.code, r'CST18_RFC_D\d{4}')

        category.code = 'TST78'

        self.assertEqual(doc.category_id.code, 'TST78')
        self.assertRegex(doc.code, r'TST78_RFC_D\d{4}')

    def test_document_code_generation_with_categ_custom_number(self):
        category = self.env['bureaucrat.knowledge.category'].create({
            'name': 'Test Categ 13',
            'code': 'CST18',
        })
        doc_type = self.env.ref(
            'bureaucrat_knowledge.bureaucrat_document_type_rfc')
        doc = self.env['bureaucrat.knowledge.document'].create({
            'name': 'Test document 123543',
            'document_format': 'html',
            'document_type_id': doc_type.id,
            'document_body_html': "<p>Test</p>",
            'document_number': 'TST13',
            'category_id': category.id,
        })

        self.assertEqual(doc.document_number, 'TST13')
        self.assertEqual(doc.code, 'CST18_RFC_TST13')

        category.code = 'TST78'

        self.assertEqual(doc.category_id.code, 'TST78')
        self.assertEqual(doc.code, 'TST78_RFC_TST13')
