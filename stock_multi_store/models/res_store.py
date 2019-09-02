##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


class ResStore(models.Model):
    _inherit = "res.store"

    warehouse_ids = fields.One2many(
        'stock.warehouse',
        'store_id',
        'Warehouses'
    )
    warehouses_count = fields.Integer(
        compute='_compute_warehouses_count',
        string='Warehouses Count',
    )

    @api.depends('warehouse_ids')
    def _compute_warehouses_count(self):
        for rec in self:
            rec.warehouses_count = len(rec.warehouse_ids)
