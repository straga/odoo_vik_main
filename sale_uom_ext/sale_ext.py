from openerp.osv import osv, fields
from openerp import api, models, _

import openerp.addons.decimal_precision as dp

import itertools
from lxml import etree
from openerp.osv.orm import setup_modifiers

import logging
_logger = logging.getLogger(__name__) # Need for message in console.





class sale_order_line(osv.osv):
    _inherit = "sale.order.line"



    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
            uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)

        if product:
            product = self.pool['product.product'].browse(cr, uid, product, context=context)
            mes_type = product.mes_type

            res['value'].update({'product_mes_type': mes_type})

            if mes_type == 'variable':
                res['value'].update({'product_uos_qty': qty_uos})
                res['value'].update({'product_uom_qty': qty})


        return res


    _columns = {


          #'product_mes_type': fields.many2one('product.mes_type', 'Type Unit of Measure ', required=True, readonly=True, states={'draft': [('readonly', False)]}),

          'product_mes_type': fields.char('Mes type'),
          'convert_coeff': fields.float('Convert coeff', digits_compute=dp.get_precision('Product Price'), help="Retail price."),

    }








