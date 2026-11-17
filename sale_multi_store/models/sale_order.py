##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    store_id = fields.Many2one(
        related="warehouse_id.store_id",
        store=True,
    )

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
        if not self.env.is_superuser() and not self.env.context.get("skip_store_filter"):
            args += ["|", ("store_id", "=", False), ("store_id", "child_of", user.store_ids.ids)]
        return super()._search(args, offset, limit, order)

    def fetch(self, field_names):
        # Since 17.0, fetch() resolves the ids through _search() as the current user, so the store
        # filter above forbids reading records of other stores (allowed up to 16.0). The filter
        # is only meant to restrict choosing records, not reading them by id.
        # keep env.company, it is part of the cache key of company-dependent fields
        records = self.with_company(self.env.company).with_context(skip_store_filter=True)
        return super(SaleOrder, records).fetch(field_names)
