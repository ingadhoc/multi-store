##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    store_id = fields.Many2one(
        'res.store',
        'Store',
        help="Store used for data analysys and also users that are not of this"
        " store, can only see this journal records but can not post or modify "
        " any entry on them."
    )
