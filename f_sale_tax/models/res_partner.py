# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_partner(models.Model):

    _inherit = "res.partner"

    f_sale_tax_ids = fields.One2many('sale.tax.control','name','Sale Tax')






