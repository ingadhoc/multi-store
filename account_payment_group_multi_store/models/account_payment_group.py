from odoo import models, fields, api


class AccountPaymentGroup(models.Model):
    _inherit = 'account.payment.group'

    store_id = fields.Many2one(
        'res.store',
        compute='_compute_store_id',
        readonly=False,
        store=True,
        # default=lambda self: self.env.user.store_id,
    )

    @api.depends('payment_ids.journal_id.store_id')
    def _compute_store_id(self):
        # tal vez en este caso buscar un store padre que de alguna manera da
        # permiso para todos estos stores?
        for rec in self:
            store = rec.payment_ids.mapped('journal_id.store_id')
            if len(store) != 1:
                continue
            rec.store_id = store

    def _get_to_pay_move_lines_domain(self):
        """ Si soy pago de un payment group con store, y :
        * el store fuerza concilacion de mismo store, entonces buscamos deuda solo de ese store
        * el store NO fuerza conciliacion de mismo store, buscamos deuda de cualquier store que no fuerce este comportamiento """
        res = super()._get_to_pay_move_lines_domain()
        if self.store_id.only_allow_reonciliaton_of_this_store:
            res += [('store_id', '=', self.store_id.id)]
        elif self.store_id:
            res += ['|', ('store_id', '=', False), ('store_id.only_allow_reonciliaton_of_this_store', '=', False)]
        return res

    @api.depends('store_id')
    def _compute_to_pay_move_lines(self):
        super()._compute_to_pay_move_lines()
