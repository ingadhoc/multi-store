##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    store_id = fields.Many2one(
        related='warehouse_id.store_id',
        store=True,
    )

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """
        Para que usuarios los usuarios no puedan elegir pickings donde no puedan
        escribir, modificamos la funcion search. No lo hacemos por regla de
        permiso ya que si no pueden ver los diarios termina dando errores en
        cualquier lugar que se use un campo related a algo del diario
        """
        user = self.env.user
        # if superadmin, do not apply
        if user.id != 1:
            args += ['|', ('store_id', '=', False), ('store_id', 'child_of', [user.store_id.id])]
        return super().search(args, offset, limit, order, count=count)
