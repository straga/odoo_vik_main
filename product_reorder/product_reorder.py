# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools.translate import _



import logging

_logger = logging.getLogger(__name__) # Need for message in console.


class ProductProduct(models.Model):
    _inherit = 'product.template'

    reorder_count = fields.Integer(string='Reorder count', compute='_compute_reorder_count', help='How many Reorders rule for product',  store=False)

    @api.one
    def _compute_reorder_count(self):
        """
        Method to compute how many reorders rule for product
        """

        #_logger.warning("Product template ID: %s", self.id )

        product_ids = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
        reorder_count = 0;
        if product_ids:
            for product_id in product_ids:
                reorder_count += self.env['stock.warehouse.orderpoint'].search_count([('product_id', '=', product_id.id)])

        self.reorder_count = reorder_count








