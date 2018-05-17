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

from dateutil import parser
import re

import pytz


from openerp.addons.backup_manager.abackup import get_server_time
#from abackup import get_server_time


from openerp import SUPERUSER_ID
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.tools import html2text
import openerp.tools as tools


from openerp.addons.yandex_disk.YaDiskClient import YaDisk
#from YaDiskClient import YaDisk

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


class db_backup_action(osv.osv):

    _name = "db.backup.action"
    _inherit = "db.backup.action"

    _columns = {

        'yadisk_backup_connector_ids': fields.one2many('yadisk.backup.connector', 'db_backup_action_id', 'Yadisk Connector'),

    }

class yadisk_odoo_connector(osv.osv):

    _name = "yadisk.odoo.connector"
    _inherit = "yadisk.odoo.connector"

    _columns = {

        'yadisk_backup_connector_ids': fields.one2many('yadisk.backup.connector', 'db_backup_action_id', 'Yadisk Connector'),

    }



class yadisk_backup_connector(osv.osv):

    _name = "yadisk.backup.connector"
    _description = "Yandex Disk Back Connector"


    _columns = {
        'name': fields.char('Description', required=True, select=True),
        'yadisk_odoo_connector_id': fields.many2one('yadisk.odoo.connector', 'Id', select=True, required=True, ondelete='cascade'),
        'db_backup_action_id': fields.many2one('db.backup.action', 'Id', select=True, ondelete='cascade'),
        'yadisk_dir': fields.char('Yadisk Directory', required=True, select=True, help="Default root /"),
        'days_save': fields.integer('Days Save', help="How many days save backup file"),
        'active_backup': fields.boolean('Active'),

    }

    _defaults = {

         'name': 'Yadisk Backup: ',
         'active_backup': True,
         'days_save': 10,
         'yadisk_dir': '/'

     }


    def daily_backup(self, cr, uid, context=None):

        context = dict(context or {})

        ya_dsk_con_obj = self.pool.get('yadisk.backup.connector')
        ya_dsk_con_search = ya_dsk_con_obj.search(cr, uid, [('active_backup', '=', True)], context=context, count=False)

        for yadisk_action in ya_dsk_con_search:

            ya_data = ya_dsk_con_obj.browse(cr, uid, yadisk_action, context=context)

            #_logger.warning("Active Action: %s", backup_action)

            yadisk_dir = ya_data.yadisk_dir

            ya_user = ya_data.yadisk_odoo_connector_id.yadisk_user
            ya_passwd = ya_data.yadisk_odoo_connector_id.yadisk_pass
            backup_dir = ya_data.db_backup_action_id.db_dir_path_id.path
            db_name = ya_data.db_backup_action_id.db_list_id.name


            tz_server = ya_data.db_backup_action_id.db_backup_source_id.tz

            server_time = get_server_time(tz_server)


            disk = YaDisk(ya_user, ya_passwd)


            try:
                ls = disk.ls(yadisk_dir)

            except Exception, e:
                error = tools.ustr(e)
                ls = False

            if not ls and yadisk_dir != '/':

                 disk.mkdir(yadisk_dir)

            source_dir = backup_dir
            filename = "%(db)s_*.*" % {'db': db_name}


            #now = datetime.datetime.today().strftime('%Y-%m-%d')
            now = server_time.strftime('%Y-%m-%d %H:%M:%S')



            dnow = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')

            for fname in glob.iglob(os.path.join(source_dir, filename)):

                modtime = os.stat(fname).st_mtime

                local_tz = pytz.timezone(tz_server)
                doutm = datetime.datetime.fromtimestamp(modtime, local_tz)

                dout = doutm.strftime('%Y-%m-%d %H:%M:%S')
                dout = datetime.datetime.strptime(dout, '%Y-%m-%d %H:%M:%S')

                #out = datetime.datetime.fromtimestamp(modtime).strftime('%Y-%m-%d %H:%M:%S')
                ##out = datetime.datetime.utcfromtimestamp(modtime).strftime('%Y-%m-%d')
                #dout = datetime.datetime.strptime(out, '%Y-%m-%d %H:%M:%S')

                _logger.warning("Check for filename: %s, Now %s - Out %s  ",fname, now, dout)
                _logger.warning("days %s  ",(dnow - dout).days)

                if (dnow - dout).days == 0:

                    disk.upload(fname, "%s/%s" % (yadisk_dir, os.path.basename(fname) ))

                    _logger.warning("Upload: %s - %s ", fname, yadisk_dir)




    def daily_housekeeping(self, cr, uid, context=None):

        context = dict(context or {})

        ya_dsk_con_obj = self.pool.get('yadisk.backup.connector')
        ya_dsk_con_search = ya_dsk_con_obj.search(cr, uid, [('active_backup', '=', True)], context=context, count=False)

        for yadisk_action in ya_dsk_con_search:

            ya_data = ya_dsk_con_obj.browse(cr, uid, yadisk_action, context=context)

            yadisk_dir = ya_data.yadisk_dir
            days_save = ya_data.days_save

            ya_user = ya_data.yadisk_odoo_connector_id.yadisk_user
            ya_passwd = ya_data.yadisk_odoo_connector_id.yadisk_pass
            backup_dir = ya_data.db_backup_action_id.db_dir_path_id.path
            db_name = ya_data.db_backup_action_id.db_list_id.name


            tz_server = ya_data.db_backup_action_id.db_backup_source_id.tz

            server_time = get_server_time(tz_server)

            disk = YaDisk(ya_user, ya_passwd)

            filename = "%(db)s_" % {'db': db_name}

            now = server_time.strftime('%Y-%m-%d %H:%M:%S')
            #now = datetime.datetime.today().strftime('%Y-%m-%d')
            dnow = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')

            ls = disk.ls(yadisk_dir)

            for yafile in ls:

                if yafile['isDir'] == False:

                    match = re.search(r'^'+filename, yafile['displayname'])

                    if match:

                        out = parser.parse(yafile['creationdate'])

                        #local_tz = pytz.timezone(tz_server) #Our Local timezone
                        #_logger.warning("local_tz: %s, Offset: %s", local_tz, tz_offset)

                        #now_utc = pytz.utc.localize(now_utc) #Add Timezone information
                        #_logger.warning("new_tz: %s", now_utc)

                        #server_time = now_utc.astimezone(local_tz) # Convert to local
                        local_tz = pytz.timezone(tz_server)
                        #dout = out.replace(tzinfo=local_tz)
                        dout = out.astimezone(local_tz) # Convert to local
                        _logger.warning("1: %s", dout)

                        dout = dout.strftime('%Y-%m-%d %H:%M:%S')
                        _logger.warning("2: %s", dout)
                        #now = datetime.datetime.today().strftime('%Y-%m-%d')
                        dout = datetime.datetime.strptime(dout, '%Y-%m-%d %H:%M:%S')
                        _logger.warning("3: %s", dout)


                        _logger.warning("file %s Dout: %s, now: %s ",yafile['displayname'], dout, dnow)

                        if (dnow - dout).days > days_save:

                            disk.rm(yafile['path'])

                            _logger.warning("file was deleted: %s ", yafile['path'])



























