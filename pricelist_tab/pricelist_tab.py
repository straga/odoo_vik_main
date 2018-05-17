# -*- coding: utf-8 -*-

from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__) # Need for message in console.

import openerp.addons.decimal_precision as dp


from lxml import etree
from openerp.osv.orm import setup_modifiers



class product_template(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    @api.one
    #@api.depends('price_version_id')
    def _compute_price_item(self):

        context = self._context or {}
        _logger.warning("context_compute: %s, ",context)
        model = self._name or {}
        id_get = context.get('product_id', False) or self.id

        _logger.warning("self.id: %s, ",self.id)

        if model and id_get:


            if model == 'product.template':

                search_field = 'product_tmpl_id'
            else:
                search_field = 'product_id'

            _logger.warning("model: %s",model)


            if not self.price_version_id.id:

                price_ver_ids = self.env['product.pricelist.version'].search([]).ids
                #_logger.warning("price_ver_ids: %s",price_ver_ids)

            else:
                _logger.warning("price_ver_ids: %s",self.price_version_id.ids)
                price_ver_ids = self.price_version_id.ids

                #price_ver_ids = list(price_ver_ids)
            _logger.warning("id_get: %s",id_get)
            _logger.warning("price_ver_ids: %s",price_ver_ids)

            related_recordset = self.env["product.pricelist.item"].search([(search_field, '=', id_get),('price_version_id', 'in', price_ver_ids ) ])
            self.prices_ids = related_recordset.ids


            _logger.warning("self.prices_ids: %s",self.prices_ids)



    price_version_id =  fields.Many2one('product.pricelist.version', 'Price List Version' )

    prices_ids =  fields.One2many('product.pricelist.item', 'product_tmpl_id', 'Prices', )
    #prices_ids = fields.One2many('product.pricelist.item','product_tmpl_id',string="Prices", compute='_compute_price_item') # todo with open filter for edit



    @api.one
    def clean_version(self):
        """ Clean Filter field"""

        self.price_version_id = None

    @api.multi
    def write(self, vals):

       # vals['price_version_id'] = None

       # super(product_template, self).write(vals)

        return True









