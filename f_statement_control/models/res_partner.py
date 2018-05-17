# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_partner(models.Model):

    _inherit = "res.partner"

    f_stat_ids = fields.One2many('statement.control','name','Statement Control')






