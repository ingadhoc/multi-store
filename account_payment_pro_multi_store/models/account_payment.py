from odoo import models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

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

    def compute_withholdings(self):
        # only compute withholdings for payment groups where the store is not disabling it
        return super(
            AccountPayment, self.filtered(lambda x: not x.store_id.dont_compute_withholdings)).compute_withholdings()

    def _compute_available_journal_ids(self):
        super()._compute_available_journal_ids()
        restrict_store = self.env['res.store'].browse(self._context.get('restrict_store_id'))
        if restrict_store:
            for rec in self:
                if restrict_store.only_allow_reonciliaton_of_this_store:
                    rec.available_journal_ids = rec.available_journal_ids.filtered(
                        lambda x: x.store_id == restrict_store)
                elif restrict_store:
                    rec.available_journal_ids = rec.available_journal_ids.filtered(
                        lambda x: not x.store_id.only_allow_reonciliaton_of_this_store)
