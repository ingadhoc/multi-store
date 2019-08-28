##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResStore(models.Model):
    _name = "res.store"
    _description = 'Stores'
    _order = 'parent_id desc, name'

    name = fields.Char(
        required=True,
    )

    parent_id = fields.Many2one(
        'res.store',
        'Parent Store',
        index=True,
    )

    child_ids = fields.One2many(
        'res.store',
        'parent_id',
        'Child Stores'
    )

    company_id = fields.Many2one(
        'res.company', 'Company',
        help='If specified, this store will be only available on selected '
        'company',
    )

    user_ids = fields.Many2many(
        'res.users',
        'res_store_users_rel',
        'cid', 'user_id',
        'Users'
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name, company_id)',
            'The store name must be unique per company!')
    ]

    @api.constrains('parent_id')
    def _check_parent_id(self):
        for rec in self:
            if not rec._check_recursion():
                raise ValidationError(
                    _('Error! You can not create recursive stores.'))

    @api.model
    def name_search(
            self, name='', args=None, operator='ilike', limit=100):
        context = dict(self._context or {})
        if context.pop('user_preference', None):
            # We browse as superuser. Otherwise, the user would be able to
            # select only the currently visible stores (according to rules,
            # which are probably to allow to see the child stores) even if
            # she belongs to some other stores.
            self = self.sudo()
            user = self.env.user
            store_ids = list(set(
                [user.store_id.id] + [cmp.id for cmp in user.store_ids]))
            args = (args or []) + [('id', 'in', store_ids)]
        return super().name_search(
            name=name, args=args, operator=operator, limit=limit)
