odoo.define('web.web_widget_colorpicker', function(require) {
    "use strict";

    var core = require('web.core');
    var widget = require('web.form_widgets');
    var FormView = require('web.FormView');
    // var list_widget_registry = core.list_widget_registry;
    // var humanizeDuration = require('humanize-duration');

    var QWeb = core.qweb;
    var _lt = core._lt;


    var FieldColorPicker = widget.FieldChar.extend({
        template: 'FieldColorPicker',
        widget_class: 'oe_form_field_color',
        is_syntax_valid: function () {
            var $input = this.$('input');
            if (!this.get("effective_readonly") && $input.size() > 0) {
                var val = $input.val();
                var isOk = /^rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d+(?:\.\d+)?))?\)$/i.test(val);
                if (!isOk) {
                    return false;
                }
                try {
                    this.parse_value(this.$('input').val(), '');
                    return true;
                } catch (e) {
                    return false;
                }
            }
            return true;
        },
        store_dom_value: function() {
            if (!this.silent) {
                if (!this.get('effective_readonly') &&
                    this.$('input').val() !== '' &&
                    this.is_syntax_valid()) {
                    // We use internal_set_value because we were called by
                    // ``.commit_value()`` which is called by a ``.set_value()``
                    // itself called because of a ``onchange`` event
                    this.internal_set_value(
                        this.parse_value(
                            this.$('input').val())
                        );
                }
            }
            },
        render_value: function () {
            var show_value = this.format_value(this.get('value'), '');
            if (!this.get("effective_readonly")) {
                var $input = this.$el.find('input');
                
                
                
                $input.val(show_value);
                // $input.css("background-color", show_value);
                // $input.addClass("colorpicker-component colorpicker");

                // <div id="cp2" class="input-group colorpicker-component">
                //     <input type="text" value="#00AABB" class="form-control" />
                //     <span class="input-group-addon"><i></i></span>
                // </div>

                // var first_bar = $('<div class="input-group colorpicker-component">' +
                //     '<input type="text" value='+show_value+' class="form-control" />' +
                //     '<span class="input-group-addon"><i></i></span>' +
                //     '</div>');
                //
                // this.$el.append(first_bar);
                this.$el.colorpicker({format: 'rgba'});
            } else {
                this.$(".oe_form_char_content").text(show_value);
                this.$('span').css("background-color", show_value);
            }
        }
    });


    core.form_widget_registry.add('colorpicker', FieldColorPicker);


    FormView.include({
        on_button_edit: function () {
            this._super();

        },
        on_button_create: function () {
            this._super();

        }
    });

    return {
        FieldColorPicker: FieldColorPicker
    };
});
