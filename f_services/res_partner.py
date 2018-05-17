# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_partner(models.Model):

    _inherit = "res.partner"

    f_task_ids = fields.One2many('fs.task','partner_id','Task', domain=[('done','=',False)])






