odoo.define('pos_product_supplier_filter.SupplierFilter', function (require) {
    "use strict";
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class SupplierFilter extends PosComponent {
        get suppliers () {
            return this.env.pos ? this.env.pos.supplier_products ? this.env.pos.supplier_products : [] : [];
        }
        filterSupplier (ev) {
            const supplier_id = $(ev.currentTarget).val();
            if (supplier_id != 0) {
                $('div.product-list article.product').addClass('hide_this_product');
                const supplier = this.env.pos.supplier_by_id[supplier_id];
                _.each(supplier.product_supplier_variant_ids, function (product_id) {
                    $(`div.product-list .product[data-product-id="${product_id}"]`).removeClass('hide_this_product');
                });
            } else {
                $('div.product-list article.product').removeClass('hide_this_product');
            }
        }
    }
    SupplierFilter.template = 'SupplierFilter';

    Registries.Component.add(SupplierFilter);

    return SupplierFilter;
});
