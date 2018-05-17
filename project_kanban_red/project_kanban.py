# -*- coding: utf-8 -*-

import logging

from openerp import tools

from openerp import models, fields, api
from openerp.tools.translate import _

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







class kanban_test(models.Model):

    _inherit = 'project.task'

    @api.onchange('date_deadline')
    def _onchange_deadline(self):

        date_deadline = self.date_deadline

        if date_deadline:


            dout = datetime.datetime.strptime(date_deadline, '%Y-%m-%d').date()
            dnow =  get_server_time()

            if (dnow - dout).days > 0 :
                self.color = 2

            else:
                self.color = 0


    def check_deadline(self, cr, uid, context=None):

        context = dict(context or {})

        project_task_obj = self.pool.get('project.task')
        project_task_search = project_task_obj.search(cr, uid, [('kanban_state', '!=', 'done')], context=context, count=False)

        for task in project_task_search:

            task_data = project_task_obj.browse(cr, uid, task, context=context)

            date_deadline = task_data.date_deadline

            if date_deadline:

                dout = datetime.datetime.strptime(date_deadline, '%Y-%m-%d').date()


                dnow = get_server_time()

                if (dnow - dout).days > 0 :

                    _logger.warning("Kanban deadline = !!!!!!!!!!!!!!!!!", )
                    project_task_obj.write(cr, uid, task, {'color': 2 }, context=None)

                else:
                    project_task_obj.write(cr, uid, task, {'color': 0 }, context=None)



