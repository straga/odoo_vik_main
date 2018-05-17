# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
import json

import logging
_logger = logging.getLogger(__name__) # Need for message in console.

class purchase_order(models.Model):
    _inherit = 'purchase.order.line'

    demander = fields.Char('Demander', compute='_compute_demander')

    @api.one
    def _compute_demander(self):
        """
        Method
        """

        data = dict()

        for procurement_id in self.procurement_ids:
            procur_name = procurement_id.name
            procur_qty = procurement_id.product_qty

            if procurement_id.move_dest_id:
                procur_name = procurement_id.move_dest_id.name
                procur_qty = procurement_id.move_dest_id.product_qty


            procur_id = procurement_id.id
            uid_id = procurement_id.create_uid.id
            uid_name = procurement_id.create_uid.name
            uid_model = procurement_id.create_uid._model._name
            uid_partner_id = procurement_id.create_uid.partner_id.id

            data[procur_id] = {

                                "uid_id": uid_id,
                                "uid_model": uid_model,
                                "uid_name": uid_name,
                                "procur_id" : procur_id,
                                "procur_name": procur_name,
                                "procur_qty":  procur_qty,
                                "uid_partner_id" : uid_partner_id
            }

        json_str = json.dumps(data)
        self.demander = json_str

