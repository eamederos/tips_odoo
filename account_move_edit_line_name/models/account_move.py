# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_line_ids = fields.One2many('account.move.line','move_id', readonly=False)

    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_ids(self):
        if self.state == 'draft':
            super()._onchange_invoice_line_ids()

    def _move_autocomplete_invoice_lines_values(self):
        ''' This method recomputes dynamic lines on the current journal entry that include taxes, cash rounding
        and payment terms lines.
        '''
        self.ensure_one()

        for line in self.line_ids.filtered(lambda l: not l.display_type):
            analytic_account = line._cache.get('analytic_account_id')

            # Do something only on invoice lines.
            if line.exclude_from_invoice_tab:
                continue

            # Shortcut to load the demo data.
            # Doing line.account_id triggers a default_get(['account_id']) that could returns a result.
            # A section / note must not have an account_id set.
            if not line._cache.get('account_id') and not line._origin:
                line.account_id = line._get_computed_account() or self.journal_id.default_account_id
            if line.product_id and not line._cache.get('name') and self.state == 'draft':
                line.name = line._get_computed_name()

            # Compute the account before the partner_id
            # In case account_followup is installed
            # Setting the partner will get the account_id in cache
            # If the account_id is not in cache, it will trigger the default value
            # Which is wrong in some case
            # It's better to set the account_id before the partner_id
            # Ensure related fields are well copied.
            if line.partner_id != self.partner_id.commercial_partner_id:
                line.partner_id = self.partner_id.commercial_partner_id
            line.date = self.date
            line.recompute_tax_line = True
            line.currency_id = self.currency_id
            if analytic_account:
                line.analytic_account_id = analytic_account

        self.line_ids._onchange_price_subtotal()
        self._recompute_dynamic_lines(recompute_all_taxes=True)

        values = self._convert_to_write(self._cache)
        values.pop('invoice_line_ids', None)
        return values



