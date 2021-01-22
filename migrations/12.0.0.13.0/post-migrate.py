def migrate(cr, installed_version):
    cr.execute("""
        UPDATE bureaucrat_knowledge_document AS bnd
        SET document_type = 'html'
        WHERE document_type is null;

        UPDATE bureaucrat_knowledge_document_history AS bnd
        SET document_type = 'html'
        WHERE document_type is null;

        UPDATE bureaucrat_knowledge_document
        SET document_body_html = temporary_document_body;

        ALTER TABLE bureaucrat_knowledge_document
        DROP COLUMN temporary_document_body;
    """)
