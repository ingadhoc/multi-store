##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    store_id = fields.Many2one(
        related='picking_type_id.store_id',
        store=True,
    )
