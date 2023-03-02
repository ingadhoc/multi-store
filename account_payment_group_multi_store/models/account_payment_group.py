from odoo import models, fields, api


class AccountPaymentGroup(models.Model):
    _inherit = 'account.payment.group'

    store_id = fields.Many2one(
        'res.store',
        # related='journal_id.store_id',
        compute='_compute_store_id',
        readonly=False,
        store=True,
        # default=lambda self: self.env.user.store_id,
    )

    @api.depends_context('to_pay_move_line_ids')
    @api.depends('payment_ids.journal_id.store_id')
    def _compute_store_id(self):
        # tal vez en este caso buscar un store padre que de alguna manera da
        # permiso para todos estos stores?
        for rec in self:
            # agregamos esto del contexto con la misma logica que esta en payment group el metodo
            # _refresh_payments_and_move_lines. Si viene eso en el contexto es porque venimos de una factura
            # y las pay lines no se refrescan.
            if self._context.get('to_pay_move_line_ids'):
                aml_store = self.env['account.move.line'].browse(self._context.get('to_pay_move_line_ids')).mapped(
                    'journal_id.store_id')
                # aca habria que verificar que no se este pagando deuda de sstores diferentes, en ese caso
                # aml_store seria > 1. Pero no siempre habria que devolver raise, porque si el store no tiene
                # store_id.only_allow_reonciliaton_of_this_store entonces no estaria mal
                rec.store_id = aml_store
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

    @api.onchange('partner_id', 'partner_type', 'company_id', 'store_id')
    def _refresh_payments_and_move_lines(self):
        return super()._refresh_payments_and_move_lines()
