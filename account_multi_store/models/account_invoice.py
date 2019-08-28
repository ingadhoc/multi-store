##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    store_id = fields.Many2one(
        related='journal_id.store_id',
        store=True,
    )
