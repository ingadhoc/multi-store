# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    store_id = fields.Many2one(
        'res.store',
        'Store',
        help="Store used for data analysys and also users that are not of this"
        " store, can only see this warehouse records but can not post or"
        " modify any record related to them."
    )


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    store_id = fields.Many2one(
        related='warehouse_id.store_id',
        store=True,
    )


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    store_id = fields.Many2one(
        related='picking_type_id.store_id',
        store=True,
    )
