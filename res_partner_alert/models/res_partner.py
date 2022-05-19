# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    contact_only_address = fields.Char(compute='_compute_contact_only_address', store=True)

    @api.depends('name', 'contact_address')
    def _compute_contact_only_address(self):
        for partner in self:
            only_address = partner.contact_address
            if partner.name:
                only_address = only_address.replace(partner.name, '')
            partner.contact_only_address = only_address

    @api.onchange('contact_address')
    def _check_contact_address_duplication(self):
        for partner in self:
            if partner.name or partner.street or partner.street2 or partner.zip or partner.country_id \
                    or partner.state_id or partner.city:
                res = {}
                domain = [('contact_only_address', 'like', partner.contact_only_address)]
                if partner.ids:
                    domain.append(('id', '!=', partner.ids[0]))
                similar = self.search(domain)
                if similar:
                    warning = {
                        'message': _("This is a possible duplicated contact")
                    }
                    res['warning'] = warning
                    return res
