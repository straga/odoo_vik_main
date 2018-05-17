function openerp_field_json_list(instance) {


    var ActionManager = instance.web.ActionManager;
    var _t = instance.web._t,

    _lt = instance.web._lt;

    var QWeb = instance.web.qweb;

    instance.web.fieldjson = instance.web.fieldjson || {};



instance.web.ListView.List.include(/** @lends instance.web.ListView.List# */{

        init: function(group, opts) {

            var self = this;
            this._super.apply(this, arguments);
            var myrui = this.$current;

            myrui.delegate('.oe_form_demander', 'click', function (e) {

               self.on_preview_view_button(e);

            })

        },

    on_preview_view_button: function(e){
        e.preventDefault();


        var am = new ActionManager(this);

        var res_id = e.target.id;


        am.do_action({

            res_model: "res.partner",
            res_id: parseInt(res_id),
            name: _t("Demander - Information"),
            type: 'ir.actions.act_window',
            view_type: 'form',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new',

        });


        return false;

        }

});


}

