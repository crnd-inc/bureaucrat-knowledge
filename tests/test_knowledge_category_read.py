from odoo import exceptions
from .test_common import TestBureaucratKnowledgeBase


class TestKnowledgeCategoryRead(TestBureaucratKnowledgeBase):

    # Testing Top level category for visibility_type = 'restricted'
    def test_category_restricted_access_read_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.visibility_user_ids), 1)
        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).name,
            'Top level category 1')

    def test_category_restricted_access_read_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.visibility_group_ids)
        self.assertFalse(self.category_top_level.visibility_user_ids)

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.visibility_group_ids), 1)
        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).name,
            'Top level category 1')

    def test_category_restricted_editors_access_read_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])

        self.category_top_level.write({
            'editor_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.editor_user_ids), 1)
        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).name,
            'Top level category 1')

    def test_category_restricted_editors_access_read_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.editor_group_ids)
        self.assertFalse(self.category_top_level.editor_user_ids)

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])

        self.category_top_level.write({
            'editor_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.editor_group_ids), 1)
        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).name,
            'Top level category 1')

    def test_category_restricted_owners_access_read_user(self):
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.owner_group_ids)
        self.assertEqual(len(self.category_top_level.owner_user_ids), 0)

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])

        self.category_top_level.write({
            'owner_user_ids': [(4, self.demo_user.id)]})

        self.assertEqual(len(self.category_top_level.owner_user_ids), 1)
        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).name,
            'Top level category 1')

    def test_category_restricted_owners_access_read_group(self):
        self.demo_user.groups_id |= self.group_demo

        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertFalse(self.category_top_level.owner_group_ids)
        self.assertEqual(len(self.category_top_level.owner_user_ids), 0)

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])

        self.category_top_level.write({
            'owner_group_ids': [(4, self.group_demo.id)]})

        self.assertEqual(len(self.category_top_level.owner_group_ids), 1)
        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).name,
            'Top level category 1')

    def test_category_public_portal_internal_access_read_user(self):
        # pylint: disable=too-many-statements
        # Initial state
        self.assertEqual(
            self.category_top_level.visibility_type, 'restricted')
        self.assertEqual(
            self.category_subcat_1.visibility_type, 'parent')
        self.assertEqual(
            self.category_subcat_2.visibility_type, 'parent')
        self.assertEqual(
            (self.category_subcat_2.actual_visibility_parent_id.
             visibility_type), 'restricted')

        # Nobody can access restricted category
        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.portal_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.public_user).read(['name'])

        # Nobody can access subcategory of restricted categ with visibility
        # type parent
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.portal_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.public_user).read(['name'])

        # Nobody can access subcategory of restricted categ with visibility
        # type parent (nesting level 2)
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.portal_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.public_user).read(['name'])

        # Change visibility to internal
        self.category_top_level.visibility_type = 'internal'

        # And check that employees could see this category
        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.public_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.portal_user).read(['name'])

        # And check that employees could see subcategory (level 1)
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.public_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.portal_user).read(['name'])

        # And check that employees could see subcategory (level 2)
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.public_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.portal_user).read(['name'])

        # Change visibility to portal
        self.category_top_level.visibility_type = 'portal'

        # And check that employees and portal users could see this category
        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        self.assertEqual(
            self.category_top_level.sudo(self.portal_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.public_user).read(['name'])

        # And check that employees and portal users could see subcategory (l1)
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.portal_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.public_user).read(['name'])

        # And check that employees and portal users could see subcategory (l2)
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')
        self.assertEqual(
            self.category_subcat_2.sudo(self.portal_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.public_user).read(['name'])

        # Change visibility to public
        self.category_top_level.visibility_type = 'public'

        # And check that employees, portal and public users could see
        # this category
        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        self.assertEqual(
            self.category_top_level.sudo(self.portal_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        self.assertEqual(
            self.category_top_level.sudo(self.public_user).read(
                ['name'])[0]['name'],
            'Top level category 1')

        # And check that employees, portal and public users could see
        # this category
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.portal_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.public_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')

        # And check that employees, portal and public users could see
        # this category
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')
        self.assertEqual(
            self.category_subcat_2.sudo(self.portal_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')
        self.assertEqual(
            self.category_subcat_2.sudo(self.public_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')

        # Change visibility time of subcategory level 1 to 'internal'
        self.category_subcat_1.visibility_type = 'internal'

        # And check that employees, portal and public users could see
        # top-level category (it has visibility type public)
        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        self.assertEqual(
            self.category_top_level.sudo(self.portal_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        self.assertEqual(
            self.category_top_level.sudo(self.public_user).read(
                ['name'])[0]['name'],
            'Top level category 1')

        # And check that only employees can see subcategory (level 1)
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.public_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.portal_user).read(['name'])

        # And check that only employees can see subcategory (level 2)
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.public_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.portal_user).read(['name'])

        # Change visibility type to 'restricted' for subcategory level 2
        self.category_subcat_2.visibility_type = 'restricted'

        # And check that nobody can see subcategory (level 2)
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.public_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.portal_user).read(['name'])

        # We can add demo_user to visibility_users and see that he can read
        # this category now
        self.category_subcat_2.visibility_user_ids |= self.demo_user
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.public_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.portal_user).read(['name'])

    # Testing subcategory 2nd level depth for visibility_type = 'restricted'
    def test_subcategory_2_restricted_access_read_user(self):
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

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.demo_user).read(['name'])

        self.category_subcat_1.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.demo_user).read(['name'])

        self.category_subcat_1.visibility_type = 'restricted'

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')

        self.category_top_level.write({
            'visibility_user_ids': [(4, self.demo_user.id)]})
        self.category_subcat_1.write({
            'visibility_user_ids': [(5, 0)],
            'visibility_type': 'parent'})

        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')

    def test_subcategory_2_restricted_access_read_group(self):
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

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.demo_user).read(['name'])

        self.category_subcat_1.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.demo_user).read(['name'])

        self.category_subcat_1.visibility_type = 'restricted'

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')

        self.category_top_level.write({
            'visibility_group_ids': [(4, self.group_demo.id)]})
        self.category_subcat_1.write({
            'visibility_group_ids': [(5, 0)],
            'visibility_type': 'parent'})

        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')

    def test_subcategory_2_restricted_editors_access_read_user(self):
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

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.demo_user).read(['name'])

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

        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')

        # We can change visibility type for subcategories to restricted,
        # and even in this case they will be visible for editors
        self.category_subcat_1.visibility_type = 'restricted'
        self.category_subcat_2.visibility_type = 'restricted'

        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')

    def test_subcategory_2_restricted_editors_access_read_group(self):
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

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.demo_user).read(['name'])

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

        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')

        # We can change visibility type for subcategories to restricted,
        # and even in this case they will be visible for editors of parent cat
        self.category_subcat_1.visibility_type = 'restricted'
        self.category_subcat_2.visibility_type = 'restricted'

        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')

    def test_subcategory_2_restricted_owners_access_read_user(self):
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

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.demo_user).read(['name'])

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

        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')

        # We can change visibility type for subcategories to restricted,
        # and even in this case they will be visible for owners of parent cat
        self.category_subcat_1.visibility_type = 'restricted'
        self.category_subcat_2.visibility_type = 'restricted'

        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')

    def test_subcategory_2_restricted_owners_access_read_group(self):
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

        with self.assertRaises(exceptions.AccessError):
            self.category_top_level.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_1.sudo(self.demo_user).read(['name'])
        with self.assertRaises(exceptions.AccessError):
            self.category_subcat_2.sudo(self.demo_user).read(['name'])

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

        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')

        # We can change visibility type for subcategories to restricted,
        # and even in this case they will be visible for owners of parent cat
        self.category_subcat_1.visibility_type = 'restricted'
        self.category_subcat_2.visibility_type = 'restricted'

        self.assertEqual(
            self.category_top_level.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Top level category 1')
        self.assertEqual(
            self.category_subcat_1.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 1')
        self.assertEqual(
            self.category_subcat_2.sudo(self.demo_user).read(
                ['name'])[0]['name'],
            'Subcategory 2')
