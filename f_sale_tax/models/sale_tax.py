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


class sale_tax_control(models.Model):

    _name = 'sale.tax.control'


    def _default_percentage(self):

        return self.env['sale.tax.percentage'].search([], limit=1)

    #@api.model
    #def _get_default_percentage(self):

       # res = self.env['sale.tax.percentage'].search([])
        #return res[0] or False
    #    return 1


    name = fields.Many2one('res.partner', 'Customer' , required=True)

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
                              ], string='Quarter', required=True)
    code = fields.Char('Code', required=True)
    account = fields.Char('Account', related='name.f_bank_acct', required=True)

    gross_sales = fields.Float("Gross Sales", required=True)
    deductions = fields.Float("Deductions", compute='_compute_deductions',)
    balance_subject_to_tax = fields.Float("Balance Subject to Tax", required=True)
    sales_tax_percentage  = fields.Many2one('sale.tax.percentage',
                                        string='Sale Tax Percentage',
                                        default=_default_percentage,
                                        required=True)

    sales_tax_due = fields.Float("Sales tax due", compute='_compute_sales_tax_due')


    _sql_constraints = [
        ('f_sale_tax_control_uniqs', 'unique(name, year, quarter)', 'Record (customer+year+quarter) must be uniq!'),
    ]




    @api.one
    @api.depends('gross_sales','balance_subject_to_tax')
    def _compute_deductions(self):
        """
        Method
        """
        deductions = 0
        if self.gross_sales and self.balance_subject_to_tax:
            deductions = self.gross_sales - self.balance_subject_to_tax

        self.deductions = deductions

    @api.one
    @api.depends('balance_subject_to_tax')
    def _compute_sales_tax_due(self):
        """
        Method
        """
        sales_tax_due = 0
        if self.balance_subject_to_tax:
            sales_tax_due = self.balance_subject_to_tax * self.sales_tax_percentage.tax_percentage

        self.sales_tax_due = sales_tax_due


class sale_tax_percentage(models.Model):
    _name = "sale.tax.percentage"

    name  = fields.Char(string='Name Tax', required=True)
    tax_percentage  = fields.Float(string='Percentage', required=True)


    _sql_constraints = [
        ('f_sale_tax_percentage', 'unique(name,tax_percentage)', 'unique = name+tax_percentage !'),
    ]