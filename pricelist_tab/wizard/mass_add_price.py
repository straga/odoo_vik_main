# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__) # Need for message in console.



class product_mass_add_price(osv.osv_memory):
    _name = 'product.mass_add_price'
    _description = 'Mass Add Price List'

    _columns = {
        'price_version_id': fields.many2one('product.pricelist.version', 'Price List Version', required=False, select=True),
        'unit_type': fields.selection([('unit', 'Unit'),('level', 'Level'),('qty', 'qty')], 'Unit Type', required=False,),

        }


    def add_price(self, cr, uid, ids, context=None):

         # get context or not
        context = context or {}

        #_logger.warning("Context = %s", context)
        prod_id_tmp = context.get('active_id')

        db_source_obj = self.pool.get('product.product')

        prod_ids = db_source_obj.search(cr, uid,
                                   [('product_tmpl_id', '=', prod_id_tmp)],
                                   context=context)

        prod_id = prod_ids[0] or {}


        #db_source_data = db_source_obj.browse(cr, uid, prod_id_tmp, context=context)

        #product_tmpl_id = db_source_data.product_tmpl_id.id
        #prod_id = db_source_data.id

        _logger.warning("prod_id = %s", prod_ids[0])
        _logger.warning("product_tmpl_id = %s", prod_id_tmp)


        # get fields from form
        res = self.read(cr, uid, ids, ['price_version_id','unit_type'], context=context)
        #convert from many record to one. get [0] level.
        res = res and res[0] or {}

        price_version_id = res['price_version_id'][0]
        # it type for circulation or blank. Determination in res.extended.
        unit_type = res['unit_type']

        if unit_type == "unit":
            try:

                self.pool.get('product.pricelist.item').create(cr, uid,
                                                 {
                                                 'name': unit_type,
                                                 'product_id': int(prod_id),
                                                 'product_tmpl_id': int(prod_id_tmp),
                                                 'min_quantity' : 0,
                                                 'sequence': 0,
                                                 'price_version_id': int(price_version_id),
                                                 'base': 1,
                                                 'price_surcharge': 0.00,
                                                 })
            except:
                return False

        else:

            try:
                # Execute the SQL command
                type_opt = unit_type
                cr.execute('select id_opt AS oid , name AS oname, value_opt as value_opt from res_extended where type_opt=%s order by 1', (type_opt,))
                data = cr.dictfetchall()


                base = 1
                if unit_type == 'qty':
                    base = 2

                rule_name2 = ''

                for rec in data:

                    rule_name1 = ''

                    oid = rec.get('oid')
                    oname = rec.get('oname','')
                    min_qty =  rec.get('value_opt')

                    rule_name = oname
                    #rule_name = type_opt + "_%s" % (oid)
                    #rule_name2 = oname

                    ## It can Direct make price rule in Price item
                    try:

                        self.pool.get('product.pricelist.item').create(cr, uid,
                                                 {
                                                 'name': rule_name,
                                                 'product_id': int(prod_id),
                                                 'product_tmpl_id': int(prod_id_tmp),
                                                 'min_quantity' : int(min_qty),
                                                 'sequence': int(oid),
                                                 'price_version_id': int(price_version_id),
                                                 'base': base,
                                                 'price_surcharge': 0.00,
                                                 })

                    except:
                        return False

            except:
                return False

        return True



