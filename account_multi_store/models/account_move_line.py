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

    def reconcile(self):
        store = None
        for line in self:
            if store is None:
                store = line.store_id
            elif line.store_id.only_allow_reonciliaton_of_this_store and store != line.store_id:
                raise UserError(_(
                    'For store "%s" you can only reconcile lines of same store') % (line.store_id.display_name))
        return super().reconcile()

    def _prepare_exchange_difference_move_vals(self, amounts_list, company=None, exchange_date=None):
        """ Ajustamos para usar diario de diferencia de cambio seteado en los stores
        """
        vals = super()._prepare_exchange_difference_move_vals(amounts_list, company=company, exchange_date=exchange_date)
        company = self.company_id or company
        if not company:
            return
        currency_exchange_journal = self.mapped('journal_id.store_id.currency_exchange_journal_id')
        if len(currency_exchange_journal) > 1:
            raise UserError(
                'Esta intentando conciliar deuda de más de un Store con distintos diarios para ajuste por diferencia '
                'de cambio\n* Stores: %s\n*Diarios: %s' % (
                    self.mapped('journal_id.store_id.name'),
                    currency_exchange_journal.mapped('name')))
        elif currency_exchange_journal:
            vals['move_vals']['journal_id'] = currency_exchange_journal.id

        return vals
