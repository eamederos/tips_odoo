from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    product_supplier_variant_ids = fields.Many2many('product.product', string='Variantes', compute='_compute_product_variants')

    def _compute_product_variants(self):
        for record in self:
            record.product_supplier_variant_ids = self.env['product.supplierinfo'].\
                search([('name','=',record.id)]).product_tmpl_id.product_variant_ids.ids or []
