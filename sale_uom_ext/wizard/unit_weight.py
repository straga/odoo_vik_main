# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__) # Need for message in console.



class smart_unit(osv.osv_memory):

    _name = 'smart.unit'
    _description = 'Add smart units and weight'


    def add_unit_weight(self, cr, uid, ids, context=None):

        # get context or not
        context = context or {}

        _logger.warning("Context = %s", context)

        # it id counter.
        counter_id = context.get('active_id')


        return True



