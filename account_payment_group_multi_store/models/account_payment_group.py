from odoo import models, fields, api


class AccountPaymentGroup(models.Model):
    _inherit = 'account.payment.group'

    store_id = fields.Many2one(
        'res.store',
        readonly=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        """ Heredamos el create por si algun codigo de ecommerce o similra crea payemtns y payments groups
        sin store y para intentar dejarlo asignado.
        Tal vez en vez de ser en el create podria ser en un action_post?
        Anteriormente estabamos conviriendo store_id a computado almacenado, pero había una suerte de recursividad
        que nos traia problemas al menos en el caso en el cual veníamos desde pagar una factura (se mostraba bien
        pero al querer agregar un pago nos recalculaba toda la deuda)
        La realidad es que si esto nos trae problemas podríamos ignorar y ni siquiera computar este dato"""
        recs = super().create(vals_list)
        for rec in recs.filtered(lambda x: not x.store_id):
            if len(rec.payment_ids.mapped('journal_id.store_id')) == 1:
                rec.store_id = rec.payment_ids.mapped('journal_id.store_id').id
            elif len(rec.to_pay_move_line_ids.mapped('journal_id.store_id')) == 1:
                rec.store_id = rec.to_pay_move_line_ids.mapped('journal_id.store_id').id
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

    @api.depends('store_id')
    def _compute_to_pay_move_lines(self):
        if self._context.get('default_to_pay_move_line_ids'):
            return
        super()._compute_to_pay_move_lines()

    def compute_withholdings(self):
        # only compute withholdings for payment groups where the store is not disabling it
        return super(
            AccountPaymentGroup, self.filtered(lambda x: not x.store_id.dont_compute_withholdings)).compute_withholdings()
