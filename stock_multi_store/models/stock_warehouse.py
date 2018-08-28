##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    store_id = fields.Many2one(
        'res.store',
        'Store',
        help="Store used for data analysys and also users that are not of this"
        " store, can only see this warehouse records but can not post or"
        " modify any record related to them."
    )
