from odoo.addons.generic_mixin.tools.migration_utils import ensure_version


@ensure_version('0.13.0')
def migrate(cr, installed_version):
    cr.execute("""
        ALTER TABLE bureaucrat_knowledge_document
        ADD COLUMN IF NOT EXISTS temporary_document_body text;

        UPDATE bureaucrat_knowledge_document
        SET temporary_document_body = (
            SELECT document_body FROM bureaucrat_knowledge_document_history
            WHERE bureaucrat_knowledge_document_history.id = latest_history_id
        );

        ALTER TABLE bureaucrat_knowledge_document_history
        RENAME COLUMN document_body TO document_body_html;
    """)
