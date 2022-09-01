##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    store_id = fields.Many2one(
        'res.store',
        'Store',
        help="Store used for data analysis and also users that are not of this"
        " store, can only see this journal records but can not post or modify "
        " any entry on them."
    )

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        """
        Para que los usuarios no puedan elegir diarios donde no puedan
        escribir, modificamos la funcion search. No lo hacemos por regla de
        permiso ya que si no pueden ver los diarios termina dando errores en
        cualquier lugar que se use un campo related a algo del diario
        """
        user = self.env.user
        # if superadmin, do not apply
        if not self.env.is_superuser():
            args += ['|', ('store_id', '=', False), ('store_id', 'child_of', [user.store_id.id])]
        return super()._search(args, offset, limit, order, count=count, access_rights_uid=access_rights_uid)
