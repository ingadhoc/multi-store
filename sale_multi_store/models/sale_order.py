##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    store_id = fields.Many2one(
        related='warehouse_id.store_id',
        store=True,
    )
