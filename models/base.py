import logging

from odoo import _, api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

SEARCH_PANEL_LIMIT = 200


class Base(models.AbstractModel):

    _inherit = 'base'

    @api.model
    def search_panel_select_range(self, field_name, **kwargs):

        field = self._fields[field_name]
        supported_types = ['many2one']
        if field.type not in supported_types:
            raise UserError(_(
                'Only types %(supported_types)s are supported for'
                ' category (found type %(field_type)s)'
            ) % ({
                'supported_types': supported_types,
                'field_type': field.type}))

        Comodel = self.env[field.comodel_name]
        fields = ['display_name']
        parent_name = (Comodel._parent_name if
                       Comodel._parent_name in Comodel._fields else False)
        if parent_name:
            fields.append(parent_name)
        return {
            'parent_field': parent_name,
            'values': (
                Comodel.with_context(
                    hierarchical_naming=False
                ).search_read([], fields, limit=SEARCH_PANEL_LIMIT)),
        }
