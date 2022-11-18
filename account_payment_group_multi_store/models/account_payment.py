from odoo import models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def _compute_available_journal_ids(self):
        super()._compute_available_journal_ids()
        for rec in self:
            if rec.payment_group_id.store_id.only_allow_reonciliaton_of_this_store:
                rec.available_journal_ids = rec.available_journal_ids.filtered(
                    lambda x: x.store_id == rec.payment_group_id.store_id)
            elif rec.payment_group_id.store_id:
                rec.available_journal_ids = rec.available_journal_ids.filtered(
                    lambda x: not x.store_id.only_allow_reonciliaton_of_this_store)

    @api.onchange('available_journal_ids')
    def _onchange_available_journal_ids(self):
        """ No es lo más elegante meter un onchange hoy en dia. Pero aca funciona y lo hacemos para que
        el primer diario que se elija en un pago sea uno de los diarios disponibles según el store.
        No vimos otra manera facil (o menos invasiva) porque odoo esto lo computa en account.move en metodo
        _compute_journal_id y en ese llamado, en el create, todavia no hay link al payment_id ni al payment_group_id.
        Podriamos mandar data por contexto pero creo que seria mas feo."""
        if not self.journal_id or self.journal_id not in self.available_journal_ids._origin:
            self.journal_id = self.available_journal_ids._origin[:1]
