##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api
from odoo.exceptions import UserError


class ResStore(models.Model):
    _inherit = "res.store"

    journal_ids = fields.One2many(
        'account.journal',
        'store_id',
        'Journals',
    )

    journals_count = fields.Integer(
        compute='_compute_journals_count',
        string='Journals Count',
    )
    currency_exchange_journal_id = fields.Many2one('account.journal')
    only_allow_reonciliaton_of_this_store = fields.Boolean(
        help='If enable, debt reconciliation will be only doable on items of this store')

    @api.depends('journal_ids')
    def _compute_journals_count(self):
        for rec in self:
            rec.journals_count = len(rec.journal_ids)

    @api.constrains('currency_exchange_journal_id')
    def _check_currency_exchange_journal_id(self):
        for rec in self.filtered('currency_exchange_journal_id'):
            if not rec.currency_exchange_journal_id.store_id:
                rec.currency_exchange_journal_id.store_id = rec.id
            elif rec.currency_exchange_journal_id.store_id != rec.id:
                raise UserError('El diario de diferencia de cambio debe ser de esta misma sucursal')
