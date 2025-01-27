##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    store_id = fields.Many2one(
        related="picking_type_id.store_id",
        store=True,
    )
