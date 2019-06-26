# -*- coding: utf-8 -*-

import logging

from odoo import tools

from odoo import models, fields, api
from odoo.tools.translate import _

import datetime
import pytz

_logger = logging.getLogger(__name__)

def get_server_time(tz_server=None):

        now_utc = datetime.datetime.utcnow() #Our UTC naive time from server,

        #_logger.warning("now_utc: %s", now_utc)

        if tz_server:

            local_tz = pytz.timezone(tz_server) #Our Local timezone
            #_logger.warning("local_tz: %s, Offset: %s", local_tz, tz_offset)

            now_utc = pytz.utc.localize(now_utc) #Add Timezone information
            #_logger.warning("new_tz: %s", now_utc)

            server_time = now_utc.astimezone(local_tz) # Convert to local
            #_logger.warning("server_time: %s", server_time)

            result = server_time
        else:
            now_utc = datetime.date.today()
            result = now_utc

        return result


class ProjectKanban(models.Model):

    _inherit = 'project.task'


    def get_color_deadline(self, date_deadline):

        dout = fields.Date.from_string(date_deadline)
        dnow = get_server_time()

        if (dnow - dout).days > 0:
            return 1
        else:
            return 0

    @api.onchange('date_deadline')
    def _onchange_deadline(self):

        date_deadline = self.date_deadline
        if date_deadline:
            self.color = self.get_color_deadline(date_deadline)

    @api.model
    def check_deadline(self):

        project_task_obj = self.env['project.task']
        project_task_search = project_task_obj.sudo().search([('kanban_state', '!=', 'done')])

        for task in project_task_search:
            date_deadline = task.date_deadline
            if date_deadline:
                color = self.get_color_deadline(date_deadline)
                task.write({'color': color})





