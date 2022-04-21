# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SaleView(models.Model):
   _name = 'sale.view'

   @api.model
   def get_sale_orders(self):
       ret_list = []
       req = ("SELECT sale_order.name, sale_order.amount_total, sale_order.state "
                   "FROM sale_order WHERE user_id = %s"%self.env.user.id)
       self.env.cr.execute(req)
       for rec in self.env.cr.dictfetchall():
           ret_list.append(rec)
       return ret_list