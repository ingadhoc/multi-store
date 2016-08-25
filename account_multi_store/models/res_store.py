# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class res_store(models.Model):
    _inherit = "res.store"

    journal_ids = fields.One2many(
        'account.journal',
        'store_id',
        'Journals'
    )
    journals_count = fields.Integer(
        compute='_compute_journals_count',
        string='Journals',
    )

    @api.one
    @api.depends('journal_ids')
    def _compute_journals_count(self):
        self.journals_count = len(self.journal_ids)
