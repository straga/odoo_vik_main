# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_partner(models.Model):

    _inherit = "res.partner"

    tax_id_number = fields.Char('Tax Id Number')
    f_pin = fields.Integer('PIN')
    f_owner = fields.Char('Owner/President')
    f_ssn = fields.Char('SSN.')
    f_dob = fields.Char('D.O.B.')
    f_driver_lic = fields.Char('Driver Lic.#')
    f_bussines_start = fields.Date('Bussines Start')
    f_fns = fields.Integer('FNS#')
    f_bank = fields.Char('Bank')
    f_routing = fields.Char('Routing')
    f_bank_acct = fields.Char('Bank ACCT')
    f_by_acct = fields.Boolean('By ACH')
    f_ammount = fields.Float('Amount')
    f_qbooks = fields.Boolean('Qbooks')










