# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class res_store(models.Model):
    _inherit = "res.store"

    warehouse_ids = fields.One2many(
        'stock.warehouse',
        'store_id',
        'Warehouses'
    )
    warehouses_count = fields.Integer(
        compute='_compute_warehouses_count',
        string='Warehouses',
    )

    @api.one
    @api.depends('warehouse_ids')
    def _compute_warehouses_count(self):
        self.warehouses_count = len(self.warehouse_ids)
