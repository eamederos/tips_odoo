from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError

class PosOrder(models.Model):
    _inherit = "pos.order"

    user_name = fields.Char(compute='_compute_user_name', store=True)

    @api.depends('user_id')
    def _compute_user_name(self):
        for order in self:
            order.user_name = order.user_id.name or ''

    @api.model
    def get_order_invoice(self, reference):
        order = self.search([('pos_reference','=',reference)])
        if order and not order.account_move:
            move_vals = order._prepare_invoice_vals()
            new_move = order._create_invoice(move_vals)
            order.write({'account_move': new_move.id, 'state': 'invoiced'})
            new_move.sudo().with_company(order.company_id)._post()
            order.account_move = new_move.id
        return order.account_move.id




