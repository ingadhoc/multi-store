##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResStore(models.Model):
    _name = "res.store"
    _description = "Stores"
    _order = "parent_id desc, name"

    name = fields.Char(
        required=True,
    )

    parent_id = fields.Many2one(
        "res.store",
        "Parent Store",
        index=True,
    )

    child_ids = fields.One2many("res.store", "parent_id", "Child Stores")

    company_id = fields.Many2one(
        "res.company",
        "Company",
        help="If specified, this store will be only available on selected " "company",
    )

    user_ids = fields.Many2many("res.users", "res_store_users_rel", "cid", "user_id", "Users")

    _sql_constraints = [("name_uniq", "unique(name, company_id)", "The store name must be unique per company!")]

    @api.constrains("parent_id")
    def _check_parent_id(self):
        for rec in self:
            if rec._has_cycle():
                raise ValidationError(_("Error! You can not create recursive stores."))

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        # usa env.context (más moderno) y asegura lista para args
        context = dict(self.env.context or {})
        args = list(args or [])
        new_self = self

        if context.pop("user_preference", None):
            # browse as superuser so the user can see all allowed stores
            stores = self.env.user.store_id + self.env.user.store_ids
            args += [("id", "in", stores.ids)]
            new_self = new_self.sudo()

        # aplica el contexto modificado antes de llamar al super
        new_self = new_self.with_context(**context)

        # Llamada por posición (no keywords) — evita el TypeError
        return super(ResStore, new_self).name_search(name, args, operator, limit)
