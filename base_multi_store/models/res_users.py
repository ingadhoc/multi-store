##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
import itertools
from itertools import repeat

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit = "res.users"

    store_id = fields.Many2one(
        "res.store",
        "Store",
        context={"user_preference": True},
        help="The store this user is currently working for.",
    )

    store_ids = fields.Many2many(
        "res.store",
        "res_store_users_rel",
        "user_id",
        "cid",
        "Stores",
    )

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ["store_id"]

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ["store_id"]

    @api.constrains("store_id", "store_ids")
    def _check_store_id(self):
        for rec in self:
            if not rec.store_id:
                continue
            if rec.store_id not in rec.store_ids:
                # Solo valida si store_ids no está vacío (evita falsos positivos al limpiar)
                if rec.store_ids:
                    raise ValidationError(_("The selected store is not allowed for your user"))

    @api.model_create_multi
    def create(self, vals_list):
        new_vals_list = []
        for values in vals_list:
            new_vals_list.append(self._remove_reified_groups(values))

        users = super().create(new_vals_list)

        # Llama al método centralizado si se están modificando las tiendas
        if any("store_ids" in vals for vals in new_vals_list):
            users._update_multi_store_group()

        return users

    def write(self, values):
        values = self._remove_reified_groups(values)

        res = super().write(values)

        # clear cache rules when store changes
        if "store_id" in values:
            self.env.registry.clear_cache()

        # Llama al método centralizado si se están modificando las tiendas
        if "store_ids" in values:
            self._update_multi_store_group()

        return res

    def _remove_reified_groups(self, values):
        """return `values` without reified group fields"""
        add, rem = [], []
        values1 = {}

        for key, val in values.items():
            if key.startswith("in_group_"):
                (add if val else rem).append(int(key[9:]))
            elif key.startswith("sel_groups_"):
                rem += [int(v) for v in key[11:].split("_")]
                if val:
                    add.append(val)
            else:
                values1[key] = val

        if "groups_id" not in values and (add or rem):
            added = self.env["res.groups"].sudo().browse(add)
            added_ids = added._ids
            # remove group ids in `rem` and add group ids in `add`
            # do not remove groups that are added by implied
            values1["groups_id"] = list(
                itertools.chain(zip(repeat(3), [gid for gid in rem if gid not in added_ids]), zip(repeat(4), add))
            )

        return values1

    def _update_multi_store_group(self):
        """
        Añade o elimina el grupo 'Multi Store' según la cantidad de tiendas
        asignadas al usuario.
        """
        group_multi_store = self.env.ref("base_multi_store.group_multi_store", False)
        if not group_multi_store:
            return

        for user in self:
            has_multiple_stores = len(user.store_ids) > 1
            in_group = group_multi_store in user.group_ids

            # Añadir grupo si tiene más de una tienda
            if has_multiple_stores and not in_group:
                user.write({"group_ids": [(4, group_multi_store.id)]})

            # Eliminar grupo si tiene una o ninguna tienda
            elif not has_multiple_stores and in_group:
                user.write({"group_ids": [(3, group_multi_store.id)]})
