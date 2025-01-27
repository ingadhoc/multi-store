from odoo import models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def _compute_available_journal_ids(self):
        super()._compute_available_journal_ids()
        restrict_store = self.env["res.store"].browse(self._context.get("restrict_store_id"))
        if restrict_store:
            for rec in self:
                if restrict_store.only_allow_reonciliaton_of_this_store:
                    rec.available_journal_ids = rec.available_journal_ids.filtered(
                        lambda x: x.store_id == restrict_store
                    )
                elif restrict_store:
                    rec.available_journal_ids = rec.available_journal_ids.filtered(
                        lambda x: not x.store_id.only_allow_reonciliaton_of_this_store
                    )
