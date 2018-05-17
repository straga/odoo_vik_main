# -*- coding: utf-8 -*-


import logging
import email

import os
import sys
import shutil
import glob
import os
import time
import datetime
import base64
import xmlrpclib


from openerp import SUPERUSER_ID
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.tools import html2text
import openerp.tools as tools


#from YaDiskClient import YaDisk
from YaDiskClient import YaDisk
#disk = YaDisk(login, password)

#disk.df() # show used and available space
#disk.ls(path) # list of files/folder with attributes
#disk.mkdir(path) # create directory
#disk.rm(path) # delete file or directory
#disk.cp(src, dst) # copy from src to dst
#disk.mv(src, dst) # move from src to dst
#disk.upload(src, dst) # upload local file src to remote file dst
#disk.download(src, dst) # download remote file src to local file dst



_logger = logging.getLogger(__name__) # Need for message in console.

class yadisk_odoo_connector(osv.osv):

    _name = "yadisk.odoo.connector"
    _description = "Yandex Disk Manager"


    _columns = {
        'name': fields.char('Description', required=True, select=True),
        'yadisk_user': fields.char('Username', size=64, required=True, help="Optional username for yandex disk"),
        'yadisk_pass': fields.char('Password', size=64, required=True, help="Optional password for yandex disk"),

        'sequence': fields.integer('Priority', help="When (smaller number = higher priority)"),
        'active_disk': fields.boolean('Active'),

        'available': fields.float('Avaible space Gb'),
        'used': fields.float('Used space Gb'),

        'yadisk_state': fields.selection([('normal', 'Normal'),('blocked', 'Error'),('done', 'Ready')], 'Yandex State', required=False),

    }

    _defaults = {
         'active_disk': True,
         'sequence': 10,
         'yadisk_state': 'normal',

     }


    def test_yadisk_connection(self, cr, uid, ids, context=None):

        res = {}

        context = dict(context or {})

        yadisk_obj = self.pool.get('yadisk.odoo.connector')
        yadisk_data = yadisk_obj.browse(cr, uid, ids, context=context)

        ya_username = yadisk_data.yadisk_user
        ya_passwd = yadisk_data.yadisk_pass

        disk = YaDisk(ya_username, ya_passwd)

        #_logger.warning("Yandex Disk: %s", disk )

        try:
            result = disk.df()

        except Exception, e:
             error = tools.ustr(e)
             result = False


        if result:

            yadisk_obj.write(cr, uid, ids, {'yadisk_state': 'done', }, context=context)

            available = result['available']
            used = result['used']

            #_logger.warning("Yandex Disk space left: %s", disk.df() )

            res['available'] = round(float(available)/1073741824, 2)

            res['used'] = round(float(used)/1073741824, 2)

            yadisk_write = yadisk_obj.write(cr, uid, ids, {'available':float(res['available']),'used':float(res['used']) ,'yadisk_state': 'done', }, context=context)

            #_logger.warning("Yandex Disk Write Info: %s", yadisk_write )

            return self.pool.get('warning').info(cr, uid, title='Yandex Disk Info:', message="Space:\n Available = %s Gb \n Used =  %s Gb "%(res['available'], res['used'] ))

        else:
            yadisk_write = yadisk_obj.write(cr, uid, ids, {'yadisk_state': 'blocked', }, context=context)

            return self.pool.get('warning').error(cr, uid, title='Yandex Disk - Check Connection', message=_("Here is what we got instead:\n %s") % error)
























