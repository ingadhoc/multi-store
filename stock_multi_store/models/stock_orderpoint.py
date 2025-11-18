##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import api, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    @api.model
    def action_open_orderpoints(self):
        res = super().action_open_orderpoints()
        user = self.env.user
        # if superadmin, do not apply
        if not self.env.is_superuser() and res.get("domain"):
            res["domain"] = res["domain"] + [
                "|",
                ("warehouse_id.store_id", "=", False),
                ("warehouse_id.store_id", "child_of", user.store_ids.ids),
            ]
        return res
