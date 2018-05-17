from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__) # Need for message in console.


WARNING_TYPES = [('warning','Warning'),('info','Information'),('error','Error')]

class warning(osv.osv_memory):
    _name = 'warning'
    _description = 'warning'
    _columns = {
        'type': fields.selection(WARNING_TYPES, string='Type', readonly=True),
        'title': fields.char(string="Title", size=100, readonly=True),
        'message': fields.text(string="Message", readonly=True),
    }
    _req_name = 'title'

    def _get_view_id(self, cr, uid):
        """Get the view id
        @return: view id, or False if no view found
        """
        res = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'warning_popup','warning_form')

        _logger.warning("1-Res: %s", res )
        return res and res[1] or False

    def nmessage(self, cr, uid, myid, context):
        mymessage = self.browse(cr, uid, myid)
        message_type = [t[1]for t in WARNING_TYPES if mymessage.type == t[0]][0]

        res = {
            'name': '%s: %s' % (_(message_type), _(mymessage.title)),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self._get_view_id(cr, uid),
            'res_model': 'warning',
            'domain': [],
            'context': context,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': mymessage.id
        }
        return res

    def warning(self, cr, uid, title, message, context=None):
        newid = self.create(cr, uid, {'title': title, 'message': message, 'type': 'warning'})
        res = self.nmessage(cr, uid, newid, context)
        return res

    def info(self, cr, uid, title, message, context=None):
        newid = self.create(cr, uid, {'title': title, 'message': message, 'type': 'info'})
        res = self.nmessage(cr, uid, newid, context)
        return res

    def error(self, cr, uid, title, message, context=None):
        newid = self.create(cr, uid, {'title': title, 'message': message, 'type': 'error'})
        res = self.nmessage(cr, uid, newid, context)
        return res
