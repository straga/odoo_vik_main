# -*- coding: utf-8 -*-


from openerp.osv import osv
from openerp.tools.translate import _

class product_product(osv.Model):
	_inherit = "product.product"

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
			
		product_default_code = self.browse(cr, uid, id, context=context)
		
		default['default_code'] = product_default_code.default_code and product_default_code.default_code + ' (copy)' or False
			
		return super(product_product, self).copy(cr, uid, id, default=default, context=context)
	
	_sql_constraints = [('default_code_unique', 'unique (default_code)','Code must be unique !')]
