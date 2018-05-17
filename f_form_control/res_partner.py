# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_partner(models.Model):

    _inherit = "res.partner"

    f_form_ids = fields.One2many('form.control','name','Task')






