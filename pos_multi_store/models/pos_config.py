##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    store_id = fields.Many2one(
        string="Store",
        comodel_name='res.store',
        compute='_compute_store_id',
        store=True,
    )

    @api.depends('stock_location_id')
    def _compute_store_id(self):
        for record in self:
            warehouse_id = record.stock_location_id.get_warehouse()
            if warehouse_id:
                record.store_id = warehouse_id.store_id
