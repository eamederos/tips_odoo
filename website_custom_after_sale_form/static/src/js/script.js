odoo.define('website_custom_after_sale_form.after_sale_form', function (require) {
'use strict';

var SaleAfterForm = AbstractAction.extend({
    contentTemplate: 'website_custom_after_sale_form.after_sale_form',
    jsLibs: [
        '/web/static/src/js/script.js',
    ],
    events: {
        'click #customer_type': 'on_click_customer_type',
    },

    on_click_customer_type: function () {
        console.log("clicking");
    },

});

core.action_registry.add('backend_sale_after_form', SaleAfterForm);

return SaleAfterForm;
});

