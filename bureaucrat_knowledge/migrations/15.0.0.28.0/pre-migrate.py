from odoo.addons.generic_mixin.tools.migration_utils import ensure_version


@ensure_version('0.28.0')
def migrate(cr, installed_version):
    cr.execute("""
        ALTER TABLE bureaucrat_knowledge_document
        ADD COLUMN document_type_id INTEGER;
    """)
