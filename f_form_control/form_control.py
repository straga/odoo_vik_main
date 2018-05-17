# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__) # Need for message in console.

import datetime
from dateutil import tz
import pytz
import time

from dateutil import rrule,relativedelta

from pdb import set_trace as bp

from openerp.exceptions import ValidationError



class form_control(models.Model):

    _name = 'form.control'

    @api.model
    def _default_partner_id(self):
        try:
            partner = self.env.context['partner_id']
            return partner

        except:
            pass


    name = fields.Many2one('res.partner', 'Customer' ,default=lambda self: self._default_partner_id(), required=True)
    form_941 = fields.Boolean(string='941')
    form_nj927 = fields.Boolean(string='NJ927')
    form_wr30 = fields.Boolean(string='WR30')
    form_sales_tax = fields.Boolean(string='SALES TAX')
    form_newark = fields.Boolean(string='NEWARK')



    year = fields.Selection( [ ('2015','2015'),
                               ('2016','2016'),
                               ('2017','2017'),
                               ('2018','2018'),
                               ('2019','2019'),
                               ('2020','2020'),
                               ('2021','2021'),
                               ('2022','2022'),
                               ('2023','2023'),
                               ], string='Year', default='2016', required=True)

    quarter = fields.Selection([
                                ('1', '1th'),
                                ('2', '2nd'),
                                ('3', '3rd'),
                                ('4', '4th'),

                              ],
                             string='Quarter', required=True)

    is_readonly = fields.Boolean(string='ReadOnly Customer and Period.')


    _sql_constraints = [
        ('f_fomr_control_uniq', 'unique(name, year, quarter)', 'Record for customer must be uniq!'),
    ]




    @api.multi
    def unlink(self):

        if self.is_readonly != True:
            super(form_control, self).unlink()
        else:
            raise ValidationError(_("Can't delete record. If forms already marked") )

        return False
