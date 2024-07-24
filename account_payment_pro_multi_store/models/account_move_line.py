# © 2016 ADHOC SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def action_register_payment(self):
        action = super().action_register_payment()
        # si todas las lineas que estoy pagando son del mismo store, mandamos el store al payment
        if len(self.mapped('journal_id.store_id')) == 1:
            action['context']['default_store_id'] = self.mapped('journal_id.store_id').id
        return action
