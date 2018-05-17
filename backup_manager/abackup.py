# -*- coding: utf-8 -*-


import logging

import os
import sys
import shutil
import glob
import os



import base64
import xmlrpclib


import time
import datetime
from dateutil import tz

import pytz


from dateutil import parser


from openerp import SUPERUSER_ID
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.tools import html2text
from openerp import netsvc
import openerp.tools as tools

from openerp import models, api

_logger = logging.getLogger(__name__) # Need for message in console.


def execute(connector, method, *args):
    res = False
    try:
        res = getattr(connector, method)(*args)
    except Exception, e:
            return False
    return res


def get_db_list(host=None, port=None):

    if host and port:
        url = 'http://' + host + ':' + port
        conn = xmlrpclib.ServerProxy(url + '/xmlrpc/db')
        db_list_name = execute(conn, 'list')
        return db_list_name
    else:
        return False

def get_server_time(tz_server):

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
            result = now_utc

        return result




class db_dir_path(osv.osv):

    _name = 'db.dir.path'
    _columns = {
                    'name': fields.char('Description', size=100, required='True'),
                    'path': fields.char('Path for BackUP', size=100, required='True'),
                    'db_backup_action_ids': fields.one2many('db.backup.action', 'db_dir_path_id', 'Backup Action'),
                }

    #_sql_constraints = [

    #]


    def test_path(self, cr, uid, ids, context=None):

        res = {}

        context = dict(context or {})

        db_dir_path_obj = self.pool.get('db.dir.path')
        db_dir_path_data = db_dir_path_obj.browse(cr, uid, ids, context=context)

        dir_name = db_dir_path_data.name
        dir_path = db_dir_path_data.path


        d = os.path.join(dir_path)

        if not os.path.exists(d):
            os.makedirs(d, 0700)
        else:
            os.chmod(d, 0700)

        return self.pool.get('warning').info(cr, uid, title='Check Availability', message="Check path for: %s  - %s, check path: %s "%( dir_name, dir_path, d))



class db_list(osv.osv):
    _name = 'db.list'
    _columns = {
                    'name' : fields.char('Description', size=100, required='True'),

                    'db_backup_action_ids': fields.one2many('db.backup.action', 'db_list_id', 'Backup Action'),
                    'db_backup_source_id': fields.many2one('db.backup.source', 'Id', select=True, ondelete='cascade'),

                }

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Database with the same name? Impossible!')
    ]



class db_backup_source(osv.osv):
    _name = 'db.backup.source'


    @api.model
    def _tz_get(self):
    # put POSIX 'Etc/*' entries at the end to avoid confusing users - see bug 1086728
        return [(tz,tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]

    @api.multi
    def _get_tz_offset(self, name, args):
        return dict(
            (p.id, datetime.datetime.now(pytz.timezone(p.tz or 'GMT')).strftime('%z'))
            for p in self)



    _columns = {
                    'host' : fields.char('Host', size=100, required='True'),
                    'port' : fields.char('Port', size=10, required='True'),
                    'name' : fields.char('Description', size=100, required='True'),
                    'admin_passwd' : fields.char('Admin password', size=100, required='True'),
                    'dbs_state': fields.selection([('normal', 'Need Test'),('blocked', 'Error'),('done', 'Ready')], 'DBs Connect State', required=False),
                    'db_backup_action_ids': fields.one2many('db.backup.action', 'db_backup_source_id', 'Backup Action'),
                    'db_list_ids': fields.one2many('db.list', 'db_backup_source_id', 'Db Name'),

                    'tz': fields.selection(_tz_get,  'Timezone Odoo Server', size=64, required='True',
                        help="TimeZone where Odoo service started. If not select will used UTC - timezone."),
                    'tz_offset': fields.function(_get_tz_offset, type='char', size=5, string='Timezone offset', invisible=True),

                }

    _defaults = {
                    'host' : lambda *a : 'localhost',
                    'port' : lambda *a : '8069',
                    'dbs_state': 'normal'
                }


    def test_dbs_connection(self, cr, uid, ids, context=None):

        res = {}

        context = dict(context or {})

        db_source_obj = self.pool.get('db.backup.source')
        db_source_data = db_source_obj.browse(cr, uid, ids, context=context)

        db_host = db_source_data.host
        db_port = db_source_data.port

        db_lists = get_db_list(db_host, db_port)
        db_list_obj = self.pool.get('db.list')

        if db_lists:

            for db_name in db_lists:

                db_list_search = db_list_obj.search(cr, uid, [('name', '=', db_name)], context=context, count=False)

                if not db_list_search:

                    values = {
                        'name': db_name,
                        'db_backup_source_id': ids[0],
                    }
                    db_list_obj.create(cr, SUPERUSER_ID, values)


            db_write = db_source_obj.write(cr, uid, ids, {'dbs_state': 'done', }, context=context)
            return self.pool.get('warning').info(cr, uid, title='Check Connection', message="Add or Update Databse List: %s "%(db_lists))

        else:
            db_write = db_source_obj.write(cr, uid, ids, {'dbs_state': 'blocked', }, context=context)
            return self.pool.get('warning').error(cr, uid, title='Check Connection', message="Wrong (Host or port) on http://%s:%s "%( db_host, db_port))

class db_backup_action(osv.osv):



    _name = "db.backup.action"
    _description = "Databse Actions Manager"

    _columns = {
        'name': fields.char('Description', required=True, select=True),
        'db_backup_source_id': fields.many2one('db.backup.source', 'Id', select=True, ondelete='cascade'),
        'db_list_id': fields.many2one('db.list', 'Id', select=True, ondelete='cascade'),
        'db_dir_path_id': fields.many2one('db.dir.path', 'Id', select=True, ondelete='cascade'),



        'sequence': fields.integer('Priority', help="When (smaller number = higher priority)"),
        'days_save': fields.integer('Days Save', help="How many days save backup file"),
        'active_backup': fields.boolean('Active'),

    }

    _defaults = {

         'name': 'Daily Backup: ',
         'active_backup': True,
         'days_save': 10,
         'sequence': 5,

     }


    def _backup_rpc(self, cr, uid, host, port,  backup_db, backup_pwd, backup_dir, tz_server=None, tz_offset=None, context = None):

        url = 'http://' + host + ':' + port
        sock = xmlrpclib.ServerProxy(url + '/xmlrpc/db')
        db_dump = base64.b64decode(sock.dump(backup_pwd, backup_db))

        server_time = get_server_time(tz_server)

        filename = "%(db)s_%(timestamp)s.dump" % {
                'db': backup_db,
                'timestamp': server_time.strftime("%Y-%m-%d_%H-%M-%SZ")
            }


        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir, 0700)
        else:
            os.chmod(backup_dir, 0700)

        backup_file = open(os.path.join(backup_dir, filename), 'w')
        backup_file.write(db_dump)
        backup_file.close()

        return filename




    def daily_backup(self, cr, uid, context=None):

        context = dict(context or {})

        backup_action_obj = self.pool.get('db.backup.action')
        backup_action_search = backup_action_obj.search(cr, uid, [('active_backup', '=', True)], context=context, count=False)

        for backup_action in backup_action_search:

            ba_data = backup_action_obj.browse(cr, uid, backup_action, context=context)

            #_logger.warning("Active Action: %s", backup_action)

            

            host = ba_data.db_backup_source_id.host
            port = ba_data.db_backup_source_id.port
            passwd = ba_data.db_backup_source_id.admin_passwd
            db_name = ba_data.db_list_id.name
            dir_path = ba_data.db_dir_path_id.path

            tz_server = ba_data.db_backup_source_id.tz
            tz_offset = ba_data.db_backup_source_id.tz_offset


            #_logger.warning("BackUP parametrs: %s, %s, %s, %s, %s, %s", host, port, db_name, dir_path, tz_server, tz_offset)

            backup_filename = self._backup_rpc(self, cr, host, port, db_name, passwd, dir_path, tz_server, tz_offset)

            _logger.warning("BackUP filename: %s", backup_filename)


    def _housekeeping(self, cr, uid, dir_path=None, days_save=None, db_name=None, tz_server=None, tz_offset=None, context=None):

        context = dict(context or {})

        source_dir = dir_path
        filename = "%(db)s_*.*" % {'db': db_name}

        server_time = get_server_time(tz_server)

        now = server_time.strftime('%Y-%m-%d %H:%M:%S')
        dnow = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')


        for fname in glob.iglob(os.path.join(source_dir, filename)):
            modtime = os.stat(fname).st_mtime

            local_tz = pytz.timezone(tz_server)
            doutm = datetime.datetime.fromtimestamp(modtime, local_tz)

            dout = doutm.strftime('%Y-%m-%d %H:%M:%S')
            dout = datetime.datetime.strptime(dout, '%Y-%m-%d %H:%M:%S')

            _logger.warning("BackUP filename Check: %s - %s - %s", fname, dout, now)

            if (dnow - dout).days > days_save:

                os.unlink(fname) #delete

                _logger.warning("Delete: %s - %s - %s", fname, dout, now)



    def daily_housekeeping(self, cr, uid, context=None):

        context = dict(context or {})

        backup_action_obj = self.pool.get('db.backup.action')
        backup_action_search = backup_action_obj.search(cr, uid, [('active_backup', '=', True)], context=context, count=False)

        for backup_action in backup_action_search:

            ba_data = backup_action_obj.browse(cr, uid, backup_action, context=context)

            days_save = ba_data.days_save
            dir_path = ba_data.db_dir_path_id.path
            db_name = ba_data.db_list_id.name

            tz_server = ba_data.db_backup_source_id.tz
            tz_offset = ba_data.db_backup_source_id.tz_offset

            self._housekeeping(cr, uid, dir_path, days_save, db_name, tz_server, tz_offset )




























