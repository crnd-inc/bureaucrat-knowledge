import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class BureaucratDocumentType(models.Model):
    _name = 'bureaucrat.document.type'
    _description = "Bureaucrat document type"
    _parent_name = 'parent_id'
    _parent_order = 'name'

    name = fields.Char(index=True, translate=True, required=True)
    code = fields.Char(index=True, required=True, Size=3)
    description = fields.Text()
    number_generator_id = fields.Many2one('ir.sequence', required=True,
                                          ondelete='restrict')

    parent_id = fields.Many2one(
        'bureaucrat.document.type', index=True, ondelete='cascade')

    document_type = fields.Selection([
        ('art', 'art'),
        ('rfc', 'Change request'),
        ('fs', 'Act of change'),
        ('ts', 'Functional specification'),
        ('sop', 'Standard operating procedure'),
        ('bpm', 'Business Process Model')], default='art')
    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         'Code name must be unique.'),
        ('code_ascii_only',
         r"CHECK (code ~ '^[a-zA-Z0-9\-_]*$')",
         'Role type code must be ascii only'),
    ]

    def name_get(self):
        result = []
        for record in self:
            rec_name = u"%(name)s [%(code)s]" % {
                'name': record.name,
                'code': record.code,
            }
            result.append((record.id, rec_name))
        return result