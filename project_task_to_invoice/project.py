# -*- coding: utf-8 -*-
from openerp.osv import fields, orm, osv


class task(osv.osv):

    _inherit = "project.task"
    _columns = {
         'invoice_task_ids': fields.one2many('account.analytic.line', 'task_id', 'Resource used'),
    }

task()


class account_analytic_line(osv.osv):
    _inherit = 'account.analytic.line'
    _description = 'Analytic Line'
    _columns = {

        'task_id': fields.many2one('project.task', 'Task', ondelete='cascade', required=False),
    }


account_analytic_line()
