##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    store_id = fields.Many2one(
        related='warehouse_id.store_id',
        store=True,
    )
