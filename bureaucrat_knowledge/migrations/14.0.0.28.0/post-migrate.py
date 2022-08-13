from odoo import api, SUPERUSER_ID
from odoo.addons.generic_mixin.tools.migration_utils import ensure_version


@ensure_version('0.28.0')
def migrate(cr, installed_version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    doc_type = env.ref(
        'bureaucrat_knowledge.bureaucrat_document_type_art',
        raise_if_not_found=False)
    if doc_type:
        env['bureaucrat.knowledge.document'].with_context(
            active_test=False
        ).search([('document_type_id', '=', False)]).write({
            'document_type_id': doc_type.id
        })
