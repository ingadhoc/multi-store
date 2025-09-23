##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, models


class StockRule(models.Model):
    _inherit = "stock.rule"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None):
        """
        Para que los usuarios no puedan elegir pickings donde no puedan
        escribir, modificamos la funcion search. No lo hacemos por regla de
        permiso ya que si no pueden ver los diarios termina dando errores en
        cualquier lugar que se use un campo related a algo del diario
        """
        user = self.env.user
        # if superadmin, do not apply
        if not self.with_user(user.id).env.is_superuser():
            args += [
                "|",
                ("warehouse_id.store_id", "=", False),
                ("warehouse_id.store_id", "child_of", [user.store_id.id]),
            ]
        return super()._search(args, offset, limit, order)
