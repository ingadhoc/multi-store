##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResStore(models.Model):
    _inherit = "res.store"

    # agregamos esta opcion para que algunos stores (tipicamente los padres)
    # no se puedan seleccionar en los grupos de pagos. Podria ser un atributo global
    # pero la verdad que en el lugar principal donde tiene sentido esto es en los grupos de pagos
    # y ademas queremos meter cambios en los otros modulos que ya estan estables
    hide_on_payments = fields.Boolean()
