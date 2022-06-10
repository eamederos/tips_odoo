odoo.define('pos_invoice_print.ReceiptScreen', function(require) {
    'use strict';

    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const Registries = require('point_of_sale.Registries');
    const contexts = require('point_of_sale.PosContext');

    const PosDteReceiptScreen = ReceiptScreen =>
        class extends ReceiptScreen {

            async printInvoice(ord) {
                var self = this;
                var order = this.env.pos.get_order();
                console.log(order);
                return this.env.pos.rpc({
                    model: 'pos.order',
                    method: 'get_order_invoice',
                   args: [order.name],
                }).then(function (result) {
                    self.env.pos.do_action('account.account_invoices', {
                        additional_context: {
                            active_ids: [result],
                        },
                    });

                });

            }
        };

    Registries.Component.extend(ReceiptScreen, PosDteReceiptScreen);

    return ReceiptScreen;
});
