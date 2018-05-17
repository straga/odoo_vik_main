function openerp_field_mask_widgets(instance) {



        instance.web.form.FieldMask = instance.web.form.FieldChar.extend({
        template : "FieldMask",


        render_value: function() {

            var show_value = this.get_value();
        	var field = this;
        	if (!field.get("effective_readonly")) {

                field.$el.find('input').val(show_value);

                var mask = field.node.attrs.mask;
                field.$el.find('input').inputmask(mask);


        	} else {

                  field.$(".oe_form_char_content").text(show_value);

        	}


        },


        get_value: function() {
        	val = this.get('value');
        	if (!val) {
        		return '';
        	}

            return  val;
        },

    });

    instance.web.form.widgets.add('mask', 'instance.web.form.FieldMask');
}

openerp.field_mask = function(openerp) {
    openerp.field_mask = openerp.field_mask || {};
    openerp_field_mask_widgets(openerp);
}

