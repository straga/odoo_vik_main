from openerp import models, fields, api
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__) # Need for message in console.

MESSAGE_TYPES = [('warning','Warning'),('info','Information'),('error','Error')]

class popup_message(models.TransientModel):
    _name = 'popup.message'
    _description = 'Popup Message'

    type = fields.Selection(MESSAGE_TYPES, string='Type', readonly=True)
    title = fields.Char(string="Title", size=100, readonly=True)
    message = fields.Text(string="Message", readonly=True)

    _req_name = 'title'

    def _get_view_id(self):
        """Get the view id
        @return: view id, or False if no view found
        """
        res = self.env['ir.model.data'].get_object_reference('popup_message','popup_message_form')

        return res and res[1] or False


    def nmessage(self, newid):

        context = (self._context or {})
        mymessage = self.search([('id', '=', newid.id)], limit=1)
        message_type = [t[1]for t in MESSAGE_TYPES if mymessage.type == t[0]][0]

        res = {
            'name': '%s: %s' % (_(message_type), _(mymessage.title)),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self._get_view_id(),
            'res_model': 'popup.message',
            'domain': [],
            'context': context,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': mymessage.id
        }


        return res

    def warning(self,title, message):
        newid = self.create({'title': title, 'message': message, 'type': 'warning'})
        res = self.nmessage(newid)
        return res

    def info(self, title, message):
        newid = self.create({'title': title, 'message': message, 'type': 'info'})
        res = self.nmessage(newid)
        return res

    def error(self, title, message):
        newid = self.create({'title': title, 'message': message, 'type': 'error'})
        res = self.nmessage(newid)
        return res
