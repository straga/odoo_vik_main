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


class license_control(models.Model):

    _name = 'license.control'


    office = fields.Char("OF.", required=True)
    name = fields.Many2one('res.partner', 'CUSTOMER' , required=True)
    city = fields.Char('CITY', required=True)
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

    state_cigarette = fields.Boolean("State Cigarette")
    state_milk = fields.Boolean("State Milk")
    state_weight = fields.Boolean("State Weight")
    city_food = fields.Boolean("City Food")
    city_milk = fields.Boolean("City Milk")
    city_cigar = fields.Boolean("City Cigar")
    city_alarm = fields.Boolean("City Alarm")
    city_ice = fields.Boolean("City Ice")
    city_fire_permit = fields.Boolean("City Fire Permit")
    health_dept = fields.Boolean("Health Dept.")
    cco = fields.Boolean("CCO")
    waste_permit = fields.Boolean("Waste Permit")


    _sql_constraints = [
        ('f_license_control_uniqs', 'unique(office, name, city, year)', 'Record (office+name+city+year) must be uniq!'),
    ]
