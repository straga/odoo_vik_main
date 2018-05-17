from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__) # Need for message in console.

import openerp.addons.decimal_precision as dp

from lxml import etree
from openerp.osv.orm import setup_modifiers
from itertools import chain
import json

import datetime
from dateutil import tz
import pytz
import time


class bom_calc(models.Model):

    _name = 'bom.calc'

    name = fields.Char(string='Name', related='product_tmp_id.name')

    product_id = fields.Many2one('product.product','Product', required=True, domain=[('type','!=','service'),('bom_ids','!=',False),('bom_ids.type','!=','phantom')])
    bom_id = fields.Many2one('mrp.bom','Bill of Material', required=True, readonly=True)

    product_tmp_id = fields.Many2one(string='Product Template',related='product_id.product_tmpl_id', readonly=True)

    calc_line_ids = fields.One2many('bom.calc.line', 'bom_calc_id', string='Lines')

    route_ids = fields.Many2many('stock.location.route', 'stock_route_bom_calc', 'product_id', 'route_id', 'Routes', domain="[('product_selectable', '=', True)]")


    product_qty = fields.Float('Product Quantity in BOM', related='bom_id.product_qty', required=False,  digits_compute=dp.get_precision('Product Unit of Measure'))
    purch_qty = fields.Float(string='Calc Purch Qty.', digits_compute= dp.get_precision('Product Price'))

    _defaults = {
        'purch_qty': 1.0,}





    @api.onchange('product_id')
    def _change_product(self):
        """ Detect chenge product"""
        res = {}
        self.bom_id = None
        return res

    def get_children(self, object, level=0): # recusive search sub level bom.
        result = []

        def _get_rec(object, level, parent=None):
            for line in object:

                res = {}
                res['p_id']         = '{}'.format(line.product_id.id)
                res['p_name']       = u'[{}] {}'.format(line.product_id.default_code or '', line.product_id.name)
                res['b_line_id']    = '{}'.format(line.id)
                res['uname']        = u'{}'.format(line.product_uom.name)
                res['level']        = '{}'.format(level)
                res['b_id']         = '{}'.format(line.bom_id.id)
                res['id_parent']     = '{}'.format(parent)  #'{}'.format('True' if line.child_line_ids else 'False') parent
                result.append(res)
                _logger.debug("ID Line: %s",line.id )
                _logger.debug("Child Line: %s",line.child_line_ids )
                _logger.debug("Parent Line: %s", parent )
                _logger.debug("Level Line: %s", level )
                _logger.debug("------: %s", "" )





                if line.child_line_ids:

                    if level<6:
                        level += 1
                        parent = line.id
                    _get_rec(line.child_line_ids,level, parent )
                    if level>0 and level<6:
                        level -= 1
                        parent = None




            return result

        children = _get_rec(object,level)

        return children


    @api.one
    def get_ids_from_bom(self):
        """ Return a list of product ids from bom """

        self.calc_line_ids.unlink()

        line_datas = self.get_children(self.bom_id.bom_line_ids)
        _logger.warning("recur BOM IDs: %s",line_datas )

        for index, line in enumerate(line_datas):

            level = int(line["level"])
            name = line["p_name"]


            for i in range(0,level):

                name = u'\u2014'+name


            var_data ={

                    'name': name,
                    'seq_line': index+1,
                    'level': level,
                    'bom_calc_id': self.id,
                    'bom_line_id' : line["b_line_id"],
                    'bom_id' : line["b_id"],
                    'id_parent' : line['id_parent']


            }
            #_logger.warning("Line: %s",index )

            res = self.env['bom.calc.line'].create(var_data)
            #_logger.warning("Line: %s",var_data )



        return ''

class bom_calc_line(models.Model):

    _name = 'bom.calc.line'

    name = fields.Char(string='Name')
    product_id = fields.Many2one('product.product','Product', related='bom_line_id.product_id')
    bom_line_id = fields.Many2one('mrp.bom.line', 'Bom Line', required=True,)


    product_qty = fields.Float('Product Quantity', related='bom_line_id.product_qty', required=False, store=True, digits_compute=dp.get_precision('Product Unit of Measure'))

    product_uom = fields.Char('UoM', compute='_compute_uom')
    bom_id = fields.Char(string='Bom')
    level = fields.Char(string='Level')
    seq_line = fields.Integer(string='Seq.')
    bom_calc_id = fields.Many2one('bom.calc', 'Bom Calc', required=True, ondelete='cascade')

    is_calc = fields.Boolean('Is Calc', compute='_compute_is_calc')

    purch_qty = fields.Float(string='Purch Qty.', compute='_compute_unit_qty', digits_compute= dp.get_precision('Product Price'))
    purch_cost = fields.Float(string='Purch Cost', compute='_compute_unit_cost', digits_compute= dp.get_precision('Product Price'))
    purch_total = fields.Float(string='Purch Total', compute='_compute_total_cost',  digits_compute= dp.get_precision('Account'))

    id_parent = fields.Char(string='Parent ID')
    id_bom_line = fields.Integer('Bom Line ID', compute='_id_bom_line', store=False)

    _order = 'seq_line'

    #_defaults = {
    #    'is_hide': True,}


    #How can over python code we can add color rule for List view
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(bom_calc_line, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)

        doc = etree.XML(res['arch'])
        #for node in doc.xpath("//field[@name='product_uom']"): #example for search field
        for node in doc.xpath("//tree[@name='color_test']"):

            node.set('colors', '#C9CACA:is_calc==False')
            setup_modifiers(node, res['fields']['is_calc'])

            #_logger.warning("Node Found: %s",node )

        res['arch'] = etree.tostring(doc)
        return res



    @api.one
    def _id_bom_line(self):
        """
        Method
        """
        #if self.is_calc:
        self.id_bom_line = self.bom_line_id.id


    @api.one
    def _compute_uom(self):
        """
        Method
        """
        #if self.is_calc:
        self.product_uom = self.bom_line_id.product_uom.name



    @api.one
    def _compute_is_calc(self):

        #versio_filter = self.bom_calc_id.versio
        #versio_product = self.product_id.iv_versio

        route_filter = self.bom_calc_id.route_ids
        route_product = self.product_id.route_ids

        #_logger.warning("Product: %s",self.product_id.name)
        #_logger.warning("--purchase: %s",self.product_id.purchase_ok)

        #up_products = self._get_bom_product(self.product_id.id)
        #_logger.warning("Return upper product: %s",up_products)


        if self.product_id.purchase_ok: #check if produc purchsase
            self.is_calc = True


            #if versio_filter.ids: # check if filter version on

                #versio_not_ok = set(versio_filter.ids).intersection(versio_product.ids)

                #_logger.warning("---PV != Filter: %s",versio_not_ok)
                #_logger.warning("------filter.ids: %s",versio_filter.ids)
                #_logger.warning("------product.ids: %s",versio_product.ids)

                #if not versio_not_ok:
                    #self.is_calc = False

                #if not versio_product:
                    #self.is_calc = False

            if route_filter.ids: # check if filter version on


                route_not_ok = set(route_filter.ids).intersection(route_product.ids)
                #_logger.warning("---PV != Filter: %s",versio_not_ok)
                #_logger.warning("------filter.ids: %s",versio_filter.ids)
                #_logger.warning("------product.ids: %s",versio_product.ids)

                if  not route_not_ok:
                    self.is_calc = False

                if  not route_filter:
                    self.is_calc = False


        else:
            self.is_calc = False




    @api.one
    def _compute_unit_qty(self):
        """
        Method
        """

        #if not self.is_calc:
        #    self.purch_qty = self.product_qty
        #else:
        _logger.debug("------: %s",self.bom_id)
        _logger.debug("   ---: %s",self.bom_calc_id.id)
        _logger.debug("   1---: %s",self.id_parent)

        if self.id_parent != 'None':

            _logger.debug("     1---: %s",self.bom_calc_id.id)
            _logger.debug("     2---: %s",self.id_parent)

            k_qty_result = self.env['bom.calc.line'].search([('bom_calc_id','=',self.bom_calc_id.id),('bom_line_id', '=',int(self.id_parent))])

            _logger.debug("     3---: %s",k_qty_result)

            k_qty = 1.0

            if k_qty_result:
                k_qty = k_qty_result[0].purch_qty

        else:
            k_qty = self.bom_calc_id.purch_qty

        _logger.debug("------k_qty: %s",k_qty)
        _logger.debug("     %s","")

        self.purch_qty = self.product_qty*k_qty


    @api.one
    def _compute_unit_cost(self):
        """
        Method
        """

        if self.is_calc:


            unit = self.bom_line_id.product_uom

            if not unit or self.product_id.uom_po_id.category_id.id != unit.category_id.id:
                unit = self.product_id.uom_po_id

            ctx = dict(self._context or {})
            if unit:
                # price_get() will respect a 'uom' in its context, in order
                # to return a default price for those units
                ctx['uom'] = unit.id

            # Compute based on pricetype
            amount_unit = self.product_id.with_context(ctx).price_get('standard_price')[self.product_id.id]

            self.purch_cost = amount_unit




        _logger.debug("------k_qty: %s",self.product_id)


    @api.one
    def _compute_total_cost(self):
        """
        Method
        """
        if self.is_calc:
            self.purch_total = self.purch_qty * self.purch_cost


















