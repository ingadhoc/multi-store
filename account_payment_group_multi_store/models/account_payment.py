from odoo import models


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
