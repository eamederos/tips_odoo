# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_line_ids = fields.One2many('account.move.line','move_id', readonly=False)

    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_ids(self):
        if self.state == 'draft':
            super()._onchange_invoice_line_ids()


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _get_computed_name(self):
        if self.parent_state == 'draft':
            return super(AccountMoveLine, self)._get_computed_name()
        else:
            return self.name