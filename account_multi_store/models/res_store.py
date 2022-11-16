##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


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
    only_allow_reonciliaton_of_this_store = fields.Boolean(
        help='If enable, debt reconciliation will be only doable on items of this store')

    @api.depends('journal_ids')
    def _compute_journals_count(self):
        for rec in self:
            rec.journals_count = len(rec.journal_ids)
