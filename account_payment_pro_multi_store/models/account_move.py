# © 2016 ADHOC SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_register_payment(self):
        action = super().action_register_payment()
        to_pay_move_lines = self.open_move_line_ids
        if len(to_pay_move_lines.mapped('journal_id.store_id')) == 1:
            action['context']['default_store_id'] = to_pay_move_lines.mapped('journal_id.store_id').id
        return action
