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

    dont_compute_withholdings = fields.Boolean()

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

    @api.model
    def _init_payment_group_multi_store_demo(self):

        # por ahora lo estamos haciendo solo para main company
        main_company = self.env.ref('base.main_company')

        store_a = self.env.ref('account_multi_store.unidad_a_store')
        # si ya configuramos diarios, seguimos adelante
        if store_a.journal_ids:
            return

        journals = self.env[('account.journal')].search([('company_id', '=', main_company.id)])
        journals.store_id = store_a.id
        
        # duplicamos todos los diarios de liquidez, venta, compra y el de diferencia de cambio
        store_b = self.env.ref('account_multi_store.unidad_b_store')
        for journal in journals.filtered(lambda x: x.type in ['sale', 'purchase', 'bank', 'cash'] or x.code == 'EXCH'):
            journal_b = journal.copy(default={'store_id': store_b.id})
            journal_b.name = '%s - B' % (journal.name)
            journal.name += ' - A'

