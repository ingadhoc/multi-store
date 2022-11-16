##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, _
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    store_id = fields.Many2one(
        related='move_id.store_id',
        store=True,
    )

    def _check_reconcile_validity(self):
        res = super()._check_reconcile_validity()
        if not self:
            return res

        store = None
        for line in self:
            if store is None:
                store = line.store_id
            elif line.store_id.only_allow_reonciliaton_of_this_store and store != line.store_id:
                raise UserError(_(
                    'For store "%s" you can only reconcile lines of same store') % (line.store_id.display_name))
        return res
