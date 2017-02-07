# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    store_id = fields.Many2one(
        'res.store',
        'Store',
        help="Store used for data analysys and also users that are not of this"
        " store, can only see this journal records but can not post or modify "
        " any entry on them."
    )


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    store_id = fields.Many2one(
        related='journal_id.store_id',
        store=True,
        readonly=True,
    )


class AccountMove(models.Model):
    _inherit = 'account.move'

    store_id = fields.Many2one(
        related='journal_id.store_id',
        store=True,
        readonly=True,
    )


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    store_id = fields.Many2one(
        related='move_id.store_id',
        store=True,
        readonly=True,
    )


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    store_id = fields.Many2one(
        related='journal_id.store_id',
        store=True,
        readonly=True,
    )
