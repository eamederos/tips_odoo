odoo.define('pos_product_supplier_filter.models', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    models.load_models([{
        model: 'res.partner',
        fields: ['name', 'product_supplier_variant_ids'],
        domain: function (self) { return [['supplier_rank','>',0]]; },
        loaded: function (self, suppliers) {
            self.supplier_products = suppliers;
            var supplier_by_id = {};
            for (var i = 0; i < suppliers.length; i++) {
                supplier_by_id[suppliers[i].id] = suppliers[i];
            }
            self.supplier_by_id = supplier_by_id;
        }
    }]);
});
