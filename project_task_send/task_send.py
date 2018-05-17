# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import logging
import email

_logger = logging.getLogger(__name__) # Need for message in console.
#_logger.warning("Task to email send = %s", send_task )

class task(osv.osv):

    _inherit = 'project.task'

    def send_mail(self, cr, uid, ids, context=None):
        email_template_obj = self.pool.get('email.template')
        template_ids = email_template_obj.search(cr, uid, [('name', '=', 'Project Task Create - Send by mail')], context=context)

        if template_ids:

            values = email_template_obj.generate_email(cr, uid, template_ids[0], ids, context=context)
            #values['attachments'] = False

            mail_mail_obj = self.pool.get('mail.mail')
            msg_id = mail_mail_obj.create(cr, uid, values, context=context)

            if msg_id:
                mail_mail_obj.send(cr, uid, [msg_id], context=context)

        return True



    def create(self, cr, uid, vals, context=None):

        new_id = super(task, self).create(cr, uid, vals, context=context)
        self.send_mail(cr, uid, new_id,)

        return new_id

task()
