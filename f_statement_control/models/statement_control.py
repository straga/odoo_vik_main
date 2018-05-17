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



class statement_control(models.Model):

    _name = 'statement.control'

    name = fields.Many2one('res.partner', 'Customer' , required=True)


    account = fields.Char('Account#')


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

    m_jan = fields.Boolean(string='Jan.')
    m_feb = fields.Boolean(string='Feb.')
    m_mar = fields.Boolean(string='Mar.')
    m_apr = fields.Boolean(string='Apr.')
    m_may = fields.Boolean(string='May.')
    m_jun = fields.Boolean(string='Jun.')
    m_jul = fields.Boolean(string='Jul.')
    m_aug = fields.Boolean(string='Aug.')
    m_sep = fields.Boolean(string='Sep.')
    m_oct = fields.Boolean(string='Oct.')
    m_nov = fields.Boolean(string='Nov.')
    m_dec = fields.Boolean(string='Dec.')



    check_image = fields.Many2one('ir.attachment', string='Check Image', domain=[('res_model','=','statement.control')])


    _sql_constraints = [
        ('f_statement_control_uniqs', 'unique(name, year)', 'Record for customer must be uniq!'),
    ]
