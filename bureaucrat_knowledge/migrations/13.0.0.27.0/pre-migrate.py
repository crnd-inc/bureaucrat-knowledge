from odoo.addons.generic_mixin.tools.migration_utils import ensure_version


@ensure_version('0.27.0')
def migrate(cr, installed_version):
    cr.execute("""
    ALTER TABLE bureaucrat_knowledge_document_history
    RENAME COLUMN document_type TO document_format;

    ALTER TABLE bureaucrat_knowledge_document
    RENAME COLUMN document_type TO document_format;
    """)
