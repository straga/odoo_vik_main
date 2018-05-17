# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__) # Need for message in console.

import datetime
from dateutil import tz
import pytz
import time

from dateutil import rrule,relativedelta





class fs_task(models.Model):

    _name = 'fs.task';


    @api.multi
    def _next_date(self, param):

        new_date = ''  # self.repeat , self.due_date , self.name

        if self.due_date:

            due_date = fields.Datetime.from_string(self.due_date)
            _logger.warning("due_date: %s",due_date )

            if self.repeat == 'daily':
                new_date = due_date+datetime.timedelta(days=1)
            if self.repeat == 'weekly':
                new_date = due_date+datetime.timedelta(weeks=1)
            if self.repeat == 'biweekly':
                new_date = due_date+datetime.timedelta(weeks=2)
            if self.repeat == 'monthly':
                new_date = due_date + relativedelta.relativedelta(months=+1)
            if self.repeat == 'bimonthly':
                new_date = due_date + relativedelta.relativedelta(months=+2)
            if self.repeat == 'quarterly':
                new_date = due_date + relativedelta.relativedelta(months=+3)
            if self.repeat == 'semiannually':
                new_date = due_date + relativedelta.relativedelta(months=+6)
            if self.repeat == 'yearly':
                new_date = due_date + relativedelta.relativedelta(months=+12)

            _logger.warning("new_date: %s",new_date )

        fs_task = self.env['fs.task']

        task = {
                'partner_id' : self.partner_id.id,
                'name': self.name,
                'due_date' : new_date,
                'repeat' : self.repeat
            }

        id_task = fs_task.create(task)
        _logger.warning("task id: %s",id_task )




    @api.model
    def create(self, vals):

        if vals.has_key('done'):

            if vals['done'] == True:
                vals['done'] = False

        new_id = super(fs_task, self).create(vals)

        return new_id

    @api.multi
    def write(self, vals):

        if vals.has_key('done'):
            if vals['done'] == True:
                vals['state'] = 'done'
        else:
            vals['state'] = 'wait'

        super(fs_task, self).write(vals)

        if vals['state'] == 'done' and self.repeat != 'no':

            self._next_date(self.repeat)


        return True

    @api.multi
    def unlink(self):

        if self.done != True:
            super(fs_task, self).unlink()

        return False

    @api.model
    def _default_partner_id(self):
        try:
            partner = self.env.context['partner_id']
            return partner

        except:
            pass



    name = fields.Text(string='Task')
    done = fields.Boolean(string='Done')
    due_date = fields.Date(string='Due Date')
    repeat = fields.Selection([('no', 'No'),
                               ('daily','Daily'),
                               ('weekly','Weekly'),
                               ('biweekly','Biweekly'),
                               ('monthly','Monthly'),
                               ('bimonthly','Bimonthly'),
                               ('quarterly','Quarterly'),
                               ('semiannually','Semiannually'),
                               ('yearly','Yearly'),
                               ], string='Repeat', default='no')

    state = fields.Selection([('wait', 'Wait'), ('done', 'Done')], string='Status',
      required=True, readonly=True, copy=False, default='wait',
      help='All')

    partner_id = fields.Many2one('res.partner', 'Customer', default=lambda self: self._default_partner_id(), readonly=True )


    _order = 'due_date'




