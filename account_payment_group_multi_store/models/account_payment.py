from odoo import models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def get_journals_domain(self):
        """ Si soy pago de un payment group con store, y :
        * el store fuerza concilacion de mismo store, entonces buscamos diarios solo de ese store
        * el store NO fuerza conciliacion de mismo store, diarios de cualquier store que no fuerce este comportamiento """
        domain = super().get_journals_domain()
        if self.payment_group_id.store_id.only_allow_reonciliaton_of_this_store:
            domain += [('store_id', '=', self.payment_group_id.store_id.id)]
        elif self.payment_group_id.store_id:
            domain += ['|', ('store_id', '=', False), ('store_id.only_allow_reonciliaton_of_this_store', '=', False)]
        return domain
