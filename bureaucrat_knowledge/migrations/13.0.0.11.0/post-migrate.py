from odoo import api, SUPERUSER_ID
from odoo.addons.generic_mixin.tools.migration_utils import ensure_version


@ensure_version('0.11.0')
def migrate(cr, installed_version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Migrate knowledge base categories
    KnowledgeCategory = env['bureaucrat.knowledge.category'].with_context(
        active_test=False)
    for record in KnowledgeCategory.search([]):
        if record.parent_id and record.visibility_type != 'parent':
            record.visibility_type = 'parent'
        elif not (record.parent_id) and record.visibility_type != 'internal':
            record.visibility_type = 'internal'

    # Migrate knowledge base documents
    KnowledgeDocument = env['bureaucrat.knowledge.document'].with_context(
        active_test=False)
    for record in KnowledgeDocument.search([]):
        if record.category_id and record.visibility_type != 'parent':
            record.visibility_type = 'parent'
        elif not (record.category_id) and record.visibility_type != 'internal':
            record.visibility_type = 'internal'
