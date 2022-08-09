##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit = 'res.users'

    store_id = fields.Many2one(
        'res.store',
        'Store',
        context={'user_preference': True},
        help='The store this user is currently working for.',
    )

    store_ids = fields.Many2many(
        'res.store',
        'res_store_users_rel',
        'user_id',
        'cid',
        'Stores',
    )

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ['store_id']

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ['store_id']

    @api.constrains('store_id', 'store_ids')
    def _check_store_id(self):
        for rec in self:
            if rec.store_id and rec.store_id not in rec.store_ids:
                raise ValidationError(
                    _("The selected store it's not allow for your user"))

    @api.model
    def create(self, values):
        values = self._remove_reified_groups(values)
        user = super().create(values)
        group_multi_store = self.env.ref(
            'base_multi_store.group_multi_store', False)
        if group_multi_store and 'store_ids' in values:
            if len(user.store_ids) <= 1 and user.id in group_multi_store.users.ids:
                user.write({'groups_id': [(3, group_multi_store.id)]})
            elif len(user.store_ids) > 1 and user.id not in group_multi_store.users.ids:
                user.write({'groups_id': [(4, group_multi_store.id)]})
        return user

    def write(self, values):
        values = self._remove_reified_groups(values)
        res = super().write(values)
        # clear cache rules when store changes
        if 'store_id' in values:
            self.env['ir.rule'].clear_caches()
        group_multi_store = self.env.ref(
            'base_multi_store.group_multi_store', False)
        if group_multi_store and 'store_ids' in values:
            for user in self:
                if len(user.store_ids) <= 1 and user.id in group_multi_store.users.ids:
                    user.write({'groups_id': [(3, group_multi_store.id)]})
                elif len(user.store_ids) > 1 and user.id not in group_multi_store.users.ids:
                    user.write({'groups_id': [(4, group_multi_store.id)]})
        return res
