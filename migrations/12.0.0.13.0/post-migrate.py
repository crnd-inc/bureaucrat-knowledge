def migrate(cr, installed_version):
    cr.execute("""
        UPDATE bureaucrat_knowledge_document AS bnd
        SET document_type = 'html'
        WHERE document_type is null;
    """)

    cr.execute("""
        UPDATE bureaucrat_knowledge_document_history AS bnd
        SET document_type = 'html'
        WHERE document_type is null;
    """)
