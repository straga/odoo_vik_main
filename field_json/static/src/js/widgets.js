function openerp_field_json_widgets(instance) {

     openerp.field_json = openerp.field_json || {};



function json_url(string, row_id) {


        var row_id = row_id;
        var obj = $.parseJSON(string || "" );
        var json_obj = obj;

        //var compiled_template = _.template('<a class="oe_form_uri" href="<%-value%>"  id="demander_<%-value4%>" > <%-value2%> <%-value3%> </a> <br>');
        //var compiled_template = _.template('<a class="oe_form_uri" href="web#id=<%=value5%>&view_type=form&model=res.partner"  id="demander_<%-value4%>" > <%-value2%> <%-value3%> </a> <br>');
        var compiled_template = _.template('<a class="oe_form_demander" href="#"  id="<%-value5%>" > <%-value2%> <%-value3%> </a> <br>');


        var list = "";

            _.each(obj, function(d_data) {

           list += compiled_template({ value2 : d_data.uid_name, value3 : d_data.procur_qty,  value5: d_data.uid_partner_id })

        });


        return list;

}





    instance.web.list.FieldJsonUrl = instance.web.list.Column.extend({


        _format: function (row_data, options) {

            if (!_.isEmpty(row_data[this.id].value)) {

                return json_url(row_data[this.id].value, row_data['id'].value);

            }

            return this._super(row_data, options);

        }
    });




    instance.web.list.columns.add('field.jsonurl', 'instance.web.list.FieldJsonUrl');



        instance.web.form.FieldJsonUrl = instance.web.form.FieldChar.extend({
        template : "JsonUrl",


        render_value: function() {

            var show_value = this.get_value();
        	var field = this;

            if (show_value) {

                 field.$el.find('input').val(json_url(show_value));
            }
            else
            {
                field.$el.find('input').val("");
            }

/*
        	if (!field.get("effective_readonly")) {

                field.$el.find('input').val(show_value);

        	} else {

                  field.$(".oe_form_char_content").text(show_value);

        	}

*/
        },


        get_value: function() {
        	val = this.get('value');
        	if (!val) {
        		return '';
        	}

            return  val;
        },

    });

    instance.web.form.widgets.add('jsonurl', 'instance.web.form.FieldJsonUrl');
}



