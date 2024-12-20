# © 2016 ADHOC SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def action_register_payment(self, ctx=None):
        action = super().action_register_payment(ctx=ctx)
        return self._apply_store_logic(action)
