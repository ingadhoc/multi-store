##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


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

    @api.multi
    def write(self, values):
        res = super().write(values)
        # clear cache rules when store changes
        if 'store_id' in values:
            self.env['ir.rule'].clear_caches()
        return res

    def __init__(self, pool, cr):
        """ Override of __init__ to add access rights on
        store fields. Access rights are disabled by
        default, but allowed on some specific fields defined in
        self.SELF_{READ/WRITE}ABLE_FIELDS.
        """
        super().__init__(pool, cr)
        # duplicate list to avoid modifying the original reference
        self.SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        self.SELF_WRITEABLE_FIELDS.append('store_id')
        # duplicate list to avoid modifying the original reference
        self.SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        self.SELF_READABLE_FIELDS.append('store_id')
