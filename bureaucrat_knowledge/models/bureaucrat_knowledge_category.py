import collections.abc
import logging
from psycopg2 import sql
from odoo import models, fields, api, tools
from odoo.addons.generic_mixin import post_write

_logger = logging.getLogger(__name__)


class BureaucratKnowledgeCategory(models.Model):
    _name = 'bureaucrat.knowledge.category'
    _description = "Bureaucrat Knowledge: Category"
    _parent_store = True
    _parent_name = 'parent_id'
    _parent_order = 'name'
    _inherit = [
        'generic.tag.mixin',
        'generic.mixin.parent.names',
        'generic.mixin.track.changes',
        'generic.mixin.data.updatable',
        'mail.thread',

    ]
    _order = 'sequence, code, name, id'
    _auto_set_noupdate_on_write = True

    name = fields.Char(translate=True, index=True, required=True)
    code = fields.Char(index=True, size=10, copy=False, required=True)
    full_name = fields.Char(compute='_compute_full_name')
    description = fields.Html()
    parent_id = fields.Many2one(
        'bureaucrat.knowledge.category', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)

    child_ids = fields.One2many(
        'bureaucrat.knowledge.category', 'parent_id')
    child_category_count = fields.Integer(
        compute='_compute_child_category_count')
    document_ids = fields.One2many(
        'bureaucrat.knowledge.document', 'category_id')
    documents_count = fields.Integer(compute='_compute_documents_count')
    active = fields.Boolean(default=True, index=True)

    category_contents = fields.Html(
        compute='_compute_category_contents')

    visibility_type = fields.Selection(
        selection=[
            ('public', 'Public'),
            ('portal', 'Portal'),
            ('internal', 'Internal'),
            ('restricted', 'Restricted'),
            ('parent', 'Parent')],
    )

    parent_ids = fields.Many2manyView(
        comodel_name='bureaucrat.knowledge.category',
        relation='bureaucrat_knowledge_category_parents_rel_view',
        column1='child_id',
        column2='parent_id',
        string='Parents Categories',
        readonly=True)

    actual_visibility_parent_id = fields.Many2one(
        'bureaucrat.knowledge.category',
        compute='_compute_actual_visibility_parent_id',
        store=True, index=True, compute_sudo=True)

    visibility_group_ids = fields.Many2many(
        comodel_name='res.groups',
        relation='bureaucrat_knowledge_category_visibility_groups',
        column1='knowledge_category_id',
        column2='group_id',
        string='Readers groups')
    visibility_user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='bureaucrat_knowledge_category_visibility_users',
        column1='knowledge_category_id',
        column2='user_id',
        string='Readers')

    editor_group_ids = fields.Many2many(
        comodel_name='res.groups',
        relation='bureaucrat_knowledge_category_editor_groups',
        column1='knowledge_category_id',
        column2='group_id',
        string='Editors groups')
    actual_editor_group_ids = fields.Many2manyView(
        comodel_name='res.groups',
        relation='bureaucrat_knowledge_category_actual_editor_groups_rel_view',
        column1='knowledge_category_id',
        column2='group_id',
        string='Actual editors groups',
        readonly=True)
    editor_user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='bureaucrat_knowledge_category_editor_users',
        column1='knowledge_category_id',
        column2='user_id',
        string='Editors')
    actual_editor_user_ids = fields.Many2manyView(
        comodel_name='res.users',
        relation='bureaucrat_knowledge_category_actual_editor_users_rel_view',
        column1='knowledge_category_id',
        column2='user_id',
        string='Actual editors',
        readonly=True)

    owner_group_ids = fields.Many2many(
        comodel_name='res.groups',
        relation='bureaucrat_knowledge_category_owner_groups',
        column1='knowledge_category_id',
        column2='group_id',
        string='Owners groups')
    actual_owner_group_ids = fields.Many2manyView(
        comodel_name='res.groups',
        relation='bureaucrat_knowledge_category_actual_owner_groups_rev_view',
        column1='knowledge_category_id',
        column2='group_id',
        string='Actual owners groups',
        readonly=True)
    owner_user_ids = fields.Many2many(
        comodel_name='res.users',
        relation='bureaucrat_knowledge_category_owner_users',
        column1='knowledge_category_id',
        column2='user_id',
        string='Owners')
    actual_owner_user_ids = fields.Many2manyView(
        comodel_name='res.users',
        relation='bureaucrat_knowledge_category_actual_owner_users_rel_view',
        column1='knowledge_category_id',
        column2='user_id',
        string='Actual owners',
        readonly=True)
    sequence = fields.Integer(default=1000, index=True)

    _sql_constraints = [
        ("check_visibility_type_parent_not_in_the_top_categories",
         "CHECK (parent_id IS NOT NULL OR"
         "(parent_id IS NULL AND visibility_type != 'parent'))",
         "Category must have a parent category"
         " to set Visibility Type 'Parent'"),
        ('code_uniq',
         'UNIQUE (code)',
         'CODE must be unique.'),
        ('code_ascii_only',
         r"CHECK (code ~ '^[a-zA-Z0-9\-_]*$')",
         'Code must be ascii only'),
    ]

    @api.depends(
        'visibility_type',
        'parent_id',
        'parent_id.visibility_type',
        'parent_ids.parent_id',
        'parent_ids.visibility_type',
    )
    def _compute_actual_visibility_parent_id(self):
        for rec in self:
            parent = rec.sudo()
            while parent.visibility_type == 'parent' and parent.parent_id:
                parent = parent.parent_id

            rec.actual_visibility_parent_id = parent

    @api.depends('child_ids')
    def _compute_child_category_count(self):
        for rec in self:
            rec.child_category_count = len(rec.child_ids)

    @api.depends('document_ids')
    def _compute_documents_count(self):
        for rec in self:
            rec.documents_count = len(rec.document_ids)

    @api.depends('child_ids', 'document_ids')
    def _compute_category_contents(self):
        tmpl = self.env.ref(
            'bureaucrat_knowledge.knowledge_category_content_template')
        for rec in self:
            if rec.child_ids or rec.document_ids:
                rec.category_contents = tmpl.render({
                    'category': rec,
                })
            else:
                rec.category_contents = False

    @api.onchange('parent_id', 'visibility_type')
    def _onchange_parent_visibility_type(self):
        for record in self:
            if record.parent_id and not record.visibility_type:
                record.visibility_type = 'parent'
            elif record.visibility_type == 'parent' and not record.parent_id:
                record.visibility_type = False

    def init(self):
        # Create relation (category_id <-> parent_category_id) as PG View
        # This relation is used to compute field parent_ids

        # Parent / child relation made flat
        tools.drop_view_if_exists(
            self.env.cr, 'bureaucrat_knowledge_category_parents_rel_view')
        self.env.cr.execute(sql.SQL("""
            CREATE or REPLACE VIEW
                bureaucrat_knowledge_category_parents_rel_view AS (
                SELECT bkc.id          AS child_id,
                       bkc_parent.id   AS parent_id
                FROM bureaucrat_knowledge_category AS bkc
                LEFT JOIN bureaucrat_knowledge_category AS bkc_parent ON (
                    bkc_parent.id::character varying IN (
                        SELECT * FROM unnest(regexp_split_to_array(
                            bkc.parent_path, '/')))
                    AND bkc_parent.id != bkc.id)
            )
        """))

        # Category m2m relations
        tools.drop_view_if_exists(
            self.env.cr,
            'bureaucrat_knowledge_category_actual_owner_groups_rev_view')
        self.env.cr.execute(sql.SQL("""
           CREATE or REPLACE VIEW
              bureaucrat_knowledge_category_actual_owner_groups_rev_view AS (
               SELECT DISTINCT
                    parent_ids.child_id AS knowledge_category_id,
                    own_group.group_id     AS group_id
               FROM bureaucrat_knowledge_category_parents_rel_view
                    AS parent_ids
               JOIN bureaucrat_knowledge_category_owner_groups AS own_group
               ON (
                    parent_ids.child_id = own_group.knowledge_category_id
                    OR
                    parent_ids.parent_id = own_group.knowledge_category_id)
            )
        """))
        tools.drop_view_if_exists(
            self.env.cr,
            'bureaucrat_knowledge_category_actual_owner_users_rel_view')
        self.env.cr.execute(sql.SQL("""
           CREATE or REPLACE VIEW
               bureaucrat_knowledge_category_actual_owner_users_rel_view AS (
               SELECT DISTINCT
                    parent_ids.child_id AS knowledge_category_id,
                    own_usr.user_id     AS user_id
               FROM bureaucrat_knowledge_category_parents_rel_view
                    AS parent_ids
               JOIN bureaucrat_knowledge_category_owner_users AS own_usr ON (
                    parent_ids.child_id = own_usr.knowledge_category_id
                    OR
                    parent_ids.parent_id = own_usr.knowledge_category_id)
            )
        """))
        tools.drop_view_if_exists(
            self.env.cr,
            'bureaucrat_knowledge_category_actual_editor_groups_rel_view')
        self.env.cr.execute(sql.SQL("""
           CREATE or REPLACE VIEW
              bureaucrat_knowledge_category_actual_editor_groups_rel_view AS (
               SELECT DISTINCT
                    parent_ids.child_id AS knowledge_category_id,
                    editor_group.group_id     AS group_id
               FROM bureaucrat_knowledge_category_parents_rel_view
                    AS parent_ids
               JOIN bureaucrat_knowledge_category_editor_groups AS editor_group
               ON (
                    parent_ids.child_id = editor_group.knowledge_category_id
                    OR
                    parent_ids.parent_id = editor_group.knowledge_category_id)
            )
        """))
        tools.drop_view_if_exists(
            self.env.cr,
            'bureaucrat_knowledge_category_actual_editor_users_rel_view')
        self.env.cr.execute(sql.SQL("""
           CREATE or REPLACE VIEW
               bureaucrat_knowledge_category_actual_editor_users_rel_view AS (
               SELECT DISTINCT
                    parent_ids.child_id AS knowledge_category_id,
                    editor_usr.user_id     AS user_id
               FROM bureaucrat_knowledge_category_parents_rel_view
                    AS parent_ids
               JOIN bureaucrat_knowledge_category_editor_users AS editor_usr
               ON (
                    parent_ids.child_id = editor_usr.knowledge_category_id
                    OR
                    parent_ids.parent_id = editor_usr.knowledge_category_id)
            )
        """))

    def _clean_caches_on_write__get_clean_fields(self, vals_list):
        """ Return set of fields, to clean caches for
        """
        to_invalidate = set()
        for vals in vals_list:
            if 'parent_id' in vals:
                to_invalidate |= {
                    'parent_ids',
                    'actual_owner_group_ids',
                    'actual_owner_user_ids',
                    'actual_editor_group_ids',
                    'actual_editor_user_ids',
                }
            if 'owner_group_ids' in vals:
                to_invalidate |= {'actual_owner_group_ids'}
            if 'owner_user_ids' in vals:
                to_invalidate |= {'actual_owner_user_ids'}
            if 'editor_group_ids' in vals:
                to_invalidate |= {'actual_editor_group_ids'}
            if 'editor_user_ids' in vals:
                to_invalidate |= {'actual_editor_user_ids'}

        return to_invalidate

    def _clean_caches_on_create_write(self, vals):
        # Invalidate cache for 'parent_ids' field
        if isinstance(vals, collections.abc.Mapping):
            to_invalidate = self._clean_caches_on_write__get_clean_fields(
                [vals])
        else:
            to_invalidate = self._clean_caches_on_write__get_clean_fields(vals)
        self.invalidate_cache(list(to_invalidate))

    @api.model_create_multi
    def create(self, vals):
        self.check_access_rights('create')

        values = []
        for v in vals:
            v = dict(v)
            if v.get('parent_id', False):
                v['visibility_type'] = 'parent'
            else:
                v['visibility_type'] = 'restricted'
                v['owner_user_ids'] = [(6, 0, [self.env.user.id])]
            values += [v]

        # create with sudo to avoid access rights error on creation, but check
        # access rights later
        categories = super(
            BureaucratKnowledgeCategory, self.sudo()).create(values)

        # It is required to recompute parent-store, because access rules relies
        # on parent-store already computed
        categories._parent_store_compute()

        # reference created category as self.env (because before this category
        # is referenced as sudo)
        categories = categories.with_env(self.env)

        # Clean caches to enforce odoo to reread fields, instead of using
        # cached (incorrect) value
        self._clean_caches_on_create_write(values)

        # Enforce check of access rights after category created,
        # to ensure that current user has access to create this category
        categories.check_access_rule('create')

        return categories

    def write(self, vals):
        res = super(BureaucratKnowledgeCategory, self).write(vals)

        self._clean_caches_on_create_write(vals)

        return res

    def action_view_subcategories(self):
        self.ensure_one()
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'bureaucrat_knowledge.action_bureaucrat_knowledge_category',
            context={'default_parent_id': self.id},
            domain=[('parent_id', '=', self.id)])

    def action_view_documents(self):
        self.ensure_one()
        return self.env['generic.mixin.get.action'].get_action_by_xmlid(
            'bureaucrat_knowledge.action_bureaucrat_knowledge_document',
            context={'default_category_id': self.id},
            domain=[('category_id', '=', self.id)])

    @post_write('active')
    def _post_active_changed(self, changes):
        for rec in self:
            self.with_context(active_test=False).search(
                [('parent_id', 'child_of', rec.id),
                 ('active', '!=', rec.active)]).write({'active': rec.active})
            self.env['bureaucrat.knowledge.document'].with_context(
                active_test=False).search(
                    [('category_id', 'child_of', rec.id),
                     ('active', '!=', rec.active)]).write(
                         {'active': rec.active})

    def name_get(self):
        result = []
        for record in self:
            rec_name = "%(name)s [%(code)s]" % {
                'name': record.name,
                'code': record.code,
            }
            result.append((record.id, rec_name))
        return result

    def _compute_full_name(self):
        def get_names(rec):
            """ Return the list [rec.name, rec.parent_id.name, ...] """
            res = []
            name_field = self._rec_name_fallback()
            while rec:
                if rec[name_field]:
                    res.append(rec[name_field])
                rec = rec[self._parent_name]
            return res
        for rec in self:
            rec.full_name = " / ".join(reversed(get_names(rec.sudo())))
