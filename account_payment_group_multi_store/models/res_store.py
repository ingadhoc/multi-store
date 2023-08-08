##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class ResStore(models.Model):
    _inherit = "res.store"

    dont_compute_withholdings = fields.Boolean()
