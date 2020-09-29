from .test_common import TestBureaucratKnowledgeBase


class TestBureaucratKnowledge(TestBureaucratKnowledgeBase):

    def test_category_default_values(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        Category = self.env['bureaucrat.knowledge.category']
        category = Category.sudo(self.user).create({
            'name': 'Test top level category',
        })

        self.assertEqual(category.visibility_type, 'restricted')
        self.assertEqual(len(category.owner_user_ids), 1)
        self.assertIn(self.user, category.owner_user_ids)
        self.assertFalse(category.editor_user_ids)

        category.write({
            'editor_user_ids': [(6, 0, [self.user.id])]})

        subcategory = Category.sudo(self.user).create({
            'name': 'Test subcategory',
            'parent_id': category.id,
        })

        self.assertEqual(len(category.editor_user_ids), 1)
        self.assertEqual(len(category.actual_editor_user_ids), 1)
        self.assertIn(self.user, category.editor_user_ids)
        self.assertIn(self.user, category.actual_editor_user_ids)
        self.assertEqual(subcategory.visibility_type, 'parent')
        self.assertEqual(len(subcategory.owner_user_ids), 1)
        self.assertIn(self.user, subcategory.owner_user_ids)

        self.assertFalse(subcategory.editor_user_ids)
        subcategory.invalidate_cache()
        self.assertEqual(len(subcategory.actual_editor_user_ids), 1)
        self.assertIn(self.user, subcategory.actual_editor_user_ids)

        subcategory2 = Category.sudo(self.user).create({
            'name': 'Test subcategory2',
            'parent_id': subcategory.id,
        })

        self.assertEqual(subcategory2.visibility_type, 'parent')
        self.assertEqual(len(subcategory2.owner_user_ids), 1)
        self.assertIn(self.user, subcategory2.owner_user_ids)
        self.assertFalse(subcategory2.editor_user_ids)
        self.assertEqual(len(subcategory2.actual_editor_user_ids), 1)
        self.assertIn(self.user, subcategory2.actual_editor_user_ids)

    def test_document_default_values(self):
        self.user.groups_id |= self.group_knowledge_user_implicit

        Document = self.env['bureaucrat.knowledge.document']
        document = Document.sudo(self.user).create({
            'name': 'Test top level document',
        })

        self.assertEqual(document.visibility_type, 'restricted')
        self.assertEqual(len(document.owner_user_ids), 1)
        self.assertIn(self.user, document.owner_user_ids)

        Category = self.env['bureaucrat.knowledge.category']
        category = Category.sudo(self.user).create({
            'name': 'Test top level category2',
        })

        category.write({
            'editor_user_ids': [(4, self.user.id)]})

        subdocument = Document.sudo(self.user).create({
            'name': 'Test top level document',
            'category_id': category.id,
        })

        self.assertEqual(subdocument.visibility_type, 'parent')
        self.assertEqual(len(subdocument.owner_user_ids), 1)
        self.assertIn(self.user, subdocument.owner_user_ids)
        self.assertFalse(subdocument.editor_user_ids)
        self.assertEqual(len(subdocument.actual_editor_user_ids), 1)
        self.assertIn(self.user, subdocument.actual_editor_user_ids)
