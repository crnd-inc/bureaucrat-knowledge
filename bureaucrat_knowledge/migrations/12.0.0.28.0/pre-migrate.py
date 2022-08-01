from odoo import api, SUPERUSER_ID
from odoo.addons.generic_mixin.tools.migration_utils import ensure_version


@ensure_version('0.28.0')
def migrate(cr, installed_version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Migrate code
    n = 0
    Category = env['bureaucrat.knowledge.category'].with_context(
        active_test=False)
    for record in Category.search([('code', '=', False)]):
        n = n + 1
        code = f'BKC_{n:04}'
        record.code = code
