from odoo.addons.generic_mixin.tools.migration_utils import ensure_version


@ensure_version('0.27.0')
def migrate(cr, installed_version):
    cr.execute("""
    ALTER TABLE bureaucrat_knowledge_document_history
    RENAME COLUMN document_type TO document_format;

    ALTER TABLE bureaucrat_knowledge_document
    RENAME COLUMN document_type TO document_format;

    UPDATE ir_model_fields
    SET name = 'document_format'
    WHERE id IN (
        SELECT res_id
        FROM ir_model_data
        WHERE module = 'bureaucrat_knowledge'
          AND name IN (
               'field_bureaucrat_knowledge_document__document_type',
               'bureaucrat_knowledge_document_history__document_type'));

    UPDATE ir_model_data
    SET name = 'field_bureaucrat_knowledge_document__document_format'
    WHERE module = 'bureaucrat_knowledge'
      AND name ='field_bureaucrat_knowledge_document__document_type';

    UPDATE ir_model_data
    SET name = 'field_bureaucrat_knowledge_document_history__document_format'
    WHERE module = 'bureaucrat_knowledge'
      AND name ='field_bureaucrat_knowledge_document_history__document_type';

    UPDATE ir_model_data
    SET name = 'selection__bureaucrat_knowledge_document__document_format__pdf'
    WHERE module = 'bureaucrat_knowledge'
      AND name ='selection__bureaucrat_knowledge_document__document_type__pdf';

    UPDATE ir_model_data
    SET name = 'selection__bureaucrat_knowledge_document_history__document_format__pdf'
    WHERE module = 'bureaucrat_knowledge'
      AND name ='selection__bureaucrat_knowledge_document_history__document_type__pdf';

    UPDATE ir_model_data
    SET name = 'selection__bureaucrat_knowledge_document__document_format__html'
    WHERE module = 'bureaucrat_knowledge'
      AND name ='selection__bureaucrat_knowledge_document__document_type__html';

    UPDATE ir_model_data
    SET name = 'selection__bureaucrat_knowledge_document_history__document_format__html'
    WHERE module = 'bureaucrat_knowledge'
      AND name ='selection__bureaucrat_knowledge_document_history__document_type__html';
    """)  # noqa: E501
