##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    store_id = fields.Many2one(
        "res.store",
        "Store",
        help="Store used for data analysis and also users that are not of this"
        " store, can only see this journal records but can not post or modify "
        " any entry on them.",
    )

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None):
        """
        Para que los usuarios no puedan elegir diarios donde no puedan
        escribir, modificamos la funcion search. No lo hacemos por regla de
        permiso ya que si no pueden ver los diarios termina dando errores en
        cualquier lugar que se use un campo related a algo del diario
        """
        user = self.env.user
        # if superadmin, do not apply
        if not self.env.is_superuser():
            domain += ["|", ("store_id", "=", False), ("store_id", "child_of", user.store_ids.ids)]
        return super(AccountJournal, self.with_context(active_test=False))._search(domain, offset, limit, order)

    @api.model
    @api.readonly
    @api.returns("self")
    def search(self, domain, offset=0, limit=None, order=None):
        user = self.env.user
        journal_ids = user.mapped("store_ids.journal_ids").ids
        if not self.with_user(user.id).env.is_superuser() and journal_ids and limit == 1:
            domain += ["|", ("store_id", "=", False), ("id", "in", journal_ids)]
        return super().search(domain, offset, limit, order)
