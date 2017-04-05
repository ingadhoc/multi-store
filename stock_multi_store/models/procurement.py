# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class ProcurementOrder(models.Model):
    _inherit = "procurement.order"

    @api.multi
    def run(self, autocommit=False):
        return super(ProcurementOrder, self.sudo()).run(autocommit=autocommit)
