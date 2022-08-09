from odoo.addons.generic_mixin.tools.migration_utils import ensure_version
from odoo.tools.sql import create_column, column_exists


def update_category_code(cr, category_id, code):
    cr.execute("""
        UPDATE bureaucrat_knowledge_category
        SET code = %(code)s
        WHERE id = %(category_id)s
    """, {
        'code': code,
        'category_id': category_id,
    })


@ensure_version('0.26.0')
def migrate(cr, installed_version):
    if not column_exists(cr, "bureaucrat_knowledge_category", 'code'):
        create_column(
            cr, "bureaucrat_knowledge_category",
            "code", "character varying(10)")

    cr.execute("""
        SELECT array_agg(id)
        FROM bureaucrat_knowledge_category
        WHERE code IS NULL
           OR code = '';

    """)
    for number, categ_id in enumerate(cr.fetchone()[0], 1):
        code = 'BKC%05d' % number
        update_category_code(cr, categ_id, code)
