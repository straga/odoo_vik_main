function openerp_field_list_url_widgets(instance) {

     openerp.field_list_url = openerp.field_list_url || {};




    instance.web.list.FieldListUrl = instance.web.list.Column.extend({


    /**
     * This RegEx matches if a string is missing a
     * standard *:// protocol prefix.
     */
    PROTOCOL_REGEX: /^(?![^:\/\/]*:?\/\/)/,

    /**
     * Format a column as a URL if the column has content.
     * Add "//" (inherit current protocol) specified in
     * RFC 1808, 2396, and 3986 if no other protocol is included.
     *
     * @param row_data record whose values should be displayed in the cell
     * @param options
     */
    _format: function(row_data, options) {
        var value = row_data[this.id].value;

        if (value) {
            return _.template("<a href='<%-href%>' target='_blank'><%-text%></a>", {
                href: value.trim().replace(this.PROTOCOL_REGEX, '//'),
                text: value
            });
        }
    }
    });

    instance.web.list.columns.add('field.ListUrl', 'instance.web.list.FieldListUrl');

}
