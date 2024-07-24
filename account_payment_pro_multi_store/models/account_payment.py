from odoo import models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.model_create_multi
    def create(self, vals_list):
        """ Heredamos el create por si algun codigo de ecommerce o similar crea payments
        sin store y para intentar dejarlo asignado.
        Tal vez en vez de ser en el create podria ser en un action_post?
        Anteriormente estabamos conviriendo store_id a computado almacenado, pero había una suerte de recursividad
        que nos traia problemas al menos en el caso en el cual veníamos desde pagar una factura (se mostraba bien
        pero al querer agregar un pago nos recalculaba toda la deuda)
        La realidad es que si esto nos trae problemas podríamos ignorar y ni siquiera computar este dato"""
        recs = super().create(vals_list)
        for rec in recs.filtered(lambda x: not x.store_id):
            if rec.journal_id.store_id:
                rec.store_id = rec.payment_ids.mapped('journal_id.store_id').id
        return recs

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

    #Funcion account_payment_pro
    @api.depends('store_id')
    def _compute_to_pay_move_lines(self):
        if self._context.get('default_to_pay_move_line_ids'):
            return
        super()._compute_to_pay_move_lines()

    def compute_withholdings(self):
        # only compute withholdings for payment groups where the store is not disabling it
        return super(
            AccountPayment, self.filtered(lambda x: not x.store_id.dont_compute_withholdings)).compute_withholdings()

    def _compute_available_journal_ids(self):
        super()._compute_available_journal_ids()
        for rec in self:
            if rec.store_id.only_allow_reonciliaton_of_this_store:
                rec.available_journal_ids = rec.available_journal_ids.filtered(
                    lambda x: x.store_id == rec.store_id)
            elif rec.store_id:
                rec.available_journal_ids = rec.available_journal_ids.filtered(
                    lambda x: not x.store_id.only_allow_reonciliaton_of_this_store)
