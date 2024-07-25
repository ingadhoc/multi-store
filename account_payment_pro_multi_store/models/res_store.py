from odoo import models, fields, api
from odoo.exceptions import UserError


class ResStore(models.Model):
    _inherit = "res.store"

    dont_compute_withholdings = fields.Boolean()

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

