from odoo import api, SUPERUSER_ID
from odoo.addons.generic_mixin.tools.migration_utils import ensure_version


@ensure_version('0.29.0')
def migrate(cr, installed_version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    docs = env['bureaucrat.knowledge.document'].with_context(
        active_test=False
    ).search([('document_number', '=', False)])
    for doc in docs:
        doc.write({
            'document_number': (
                doc.document_type_id.number_generator_id.next_by_id()),
        })
