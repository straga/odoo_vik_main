openerp.pos_sort = function(instance){

    var module = instance.point_of_sale;

    pos_sort_at(instance, module);
    pos_sort_bt(instance, module);




};

openerp.field_json = function(openerp) {


    openerp_field_json_widgets(openerp);
    openerp_field_json_list(openerp);
}