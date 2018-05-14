##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, SUPERUSER_ID
from odoo.osv import osv


class res_store(models.Model):
    _name = "res.store"
    _description = 'Stores'
    _order = 'parent_id desc, name'

    name = fields.Char(
        'Name',
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
        # required=True,
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

    _constraints = [
        (osv.osv._check_recursion,
         'Error! You can not create recursive stores.', ['parent_id'])
    ]

    # Copy from res_company
    def name_search(
            self, cr, uid, name='', args=None, operator='ilike',
            context=None, limit=100):
        context = dict(context or {})
        if context.pop('user_preference', None):
            # We browse as superuser. Otherwise, the user would be able to
            # select only the currently visible stores (according to rules,
            # which are probably to allow to see the child stores) even if
            # she belongs to some other stores.
            user = self.pool.get('res.users').browse(
                cr, SUPERUSER_ID, uid, context=context)
            store_ids = list(set(
                [user.store_id.id] + [cmp.id for cmp in user.store_ids]))
            uid = SUPERUSER_ID
            args = (args or []) + [('id', 'in', store_ids)]
        return super(res_store, self).name_search(
            cr, uid, name=name, args=args, operator=operator,
            context=context, limit=limit)
