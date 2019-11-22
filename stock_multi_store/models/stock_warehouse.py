##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    store_id = fields.Many2one(
        'res.store',
        'Store',
        help="Store used for data analysys and also users that are not of this"
        " store, can only see this warehouse records but can not post or"
        " modify any record related to them."
    )

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """
        Para que usuarios los usuarios no puedan elegir almacenes donde no puedan
        escribir, modificamos la funcion search. No lo hacemos por regla de
        permiso ya que si no pueden ver los diarios termina dando errores en
        cualquier lugar que se use un campo related a algo del diario
        """
        user = self.env.user
        # if superadmin, do not apply
        if user.id != 1:
            args += ['|', ('store_id', '=', False), ('store_id', 'child_of', [user.store_id.id])]
        return super().search(args, offset, limit, order, count=count)
