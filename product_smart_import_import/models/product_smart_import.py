# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime
import base64
import os

import logging
_logger = logging.getLogger(__name__)
try:
    import xlrd
except (ImportError, IOError):
    plt = False
    _logger.warning('Missing library xlrd.')
import logging
_logger = logging.getLogger(__name__)

class SalImport(models.Model):
    _name = 'product.smart.import'
    _description = 'Sale Order Import'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _smart = "id desc"

    name = fields.Char("Reference", required=True, default=_('New'), copy=False)
    import_lines = fields.One2many('product.smart.import.line', 'import_id',copy=True)
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('validated', 'Validado'), ('category', 'Categorías'),('attribute','Atributos'), ('template','Pantilla Producto'),('variant','Variante Producto'),('done', 'Hecho'), ('cancel', 'Cancelado'), ('error', 'Error')],
        string='Estado', default='draft', tracking=True)
    user_id = fields.Many2one('res.users', string='Usuario', readonly=True, index=True, tracking=True, required=True,
                              default=lambda self: self.env.user)
    next_id = fields.Many2one('product.smart.import', string="Próximo")
    error_log = fields.Text(copy=False)
    file = fields.Binary('Fichero Ventas')
    file_name = fields.Char('File name')
    active = fields.Boolean(default=True)
    product_template_ids = fields.Many2many('product.template',copy=False)
    limit = fields.Integer('Límite', default=100, required=True)

    def back_to_validated(self):
        self.state = 'validated'

    def unlink(self):
        for record in self:
            if record.state not in ['draft']:
                raise UserError("Importadores de Ventas sólo pueden ser eliminados desde estado borrador")
        return super().unlink()

    @api.constrains('active')
    def _check_active(self):
        for record in self:
            if not record.active and record.state not in ['draft']:
                raise UserError("Importadores de Ventas sólo pueden ser archivados desde estado borrador")

    @api.onchange('file')
    def onchange_file(self):
       self.import_lines.unlink()

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('product.smart.import') or _('New')
        return super().create(vals)

    # def action_view_smarts(self):
    #     smarts = self.mapped('smart_ids')
    #     action = self.env.ref('product.action_smarts').sudo().read()[0]
    #     action['domain'] = [('id', 'in', smarts.ids)]
    #     return action

    @api.model
    def excel_validator(self, xml_name):
        name, extension = os.path.splitext(xml_name)
        return True if extension in ['.xlsx','.xls'] else False

    def action_import_file(self):
        if not self.file:
            raise UserError("Es necesario un Fichero para Importar")
        if not self.excel_validator(self.file_name):
            raise UserError(_("File must contain excel extension"))
        self.import_excel_file()

    def action_validate(self):
        if len(self.import_lines) == 0:
            raise UserError("No hay líneas para validar")
        self.state = 'validated'

    def check_completed_execution(self):
        lines = self.import_lines.filtered_domain([('executed','=',False)])
        if len(lines) == 0:
            self.import_lines.write({'executed': False})
            return True
        return False

    def import_excel_file(self):
        self.import_lines.unlink()
        data = base64.b64decode(self.file)
        work_book = xlrd.open_workbook(file_contents=data)
        sheet = work_book.sheet_by_index(0)
        LineObj = self.env['product.smart.import.line']
        first_row = []
        row_count = 0
        for col in range(sheet.ncols):
            first_row.append(sheet.cell_value(0, col))
        for count, row in enumerate(range(1, sheet.nrows), 2):
            row_count += 1
            val = {}
            for col in range(sheet.ncols):
                val[first_row[col]] = sheet.cell_value(row, col)

            vals = self._prepare_future_smart_vals(val)
            LineObj.create(vals)

    def _prepare_future_smart_vals(self, val):
        product_code = str(val['Código'])
        code_splitted = product_code.split('.')
        if len(code_splitted) > 1:
            product_code = code_splitted[0]
        vals = {
            'product_code': product_code,
            'import_id': self.id,
        }
        product_name = ''
        for element in val:
            if 'Nombre' in element and val[element] not in (0,''):
                product_name += "%s "%str(val[element])
        try:
            vals.update({'product_name': product_name})
        except:
            pass
        try:
            category_name = str(val['Familia'])
            if category_name not in (0,''):
                vals.update({'category_name': category_name})
        except:
            pass
        try:
            color = str(val['Color'])
            if color not in (0,''):
                vals.update({'color': color})
        except:
            pass
        try:
            size = str(val['Talla'])
            if size not in (0,''):
                vals.update({'size': size})
        except:
            pass
        try:
            size_2 = str(val['Tamaño'])
            if size_2 not in (0,''):
                vals.update({'size_2': size_2})
        except:
            pass
        try:
            measure = str(val['Medidas'])
            if measure not in (0,''):
                vals.update({'measure': measure})
        except:
            pass
        try:
            price = str(val['Precio'])
            if price not in (''):
                vals.update({'price': float(price)})
        except:
            pass
        return vals

    def action_execute_cron(self):
        _logger.info(':::::::: COMENZANDO CRON PARA IMPORTAR NOGUERO :::::::::::::::::')
        imports = self.search([('state','=','validated')])
        try:
            for imp in imports:
                imp.action_create_product()
        except:
            pass
        _logger.info(':::::::: TERMINANDO CRON PARA IMPORTAR NOGUERO :::::::::::::::::')

    def action_draft(self):
        self.import_lines.write({'product_template_id': False, 'product_id': False,'executed': False,'error': ''})
        self.state = 'draft'

    def process_categories(self):
        count = 0
        Category_Obj = self.env['product.category']
        for line in self.import_lines.filtered_domain([('executed','=',False)]):
            if count < self.limit:
                line._create_category(Category_Obj)
                count += 1
                line.executed = True
            else:
                break
        if self.check_completed_execution():
            self.state = 'category'

    def process_attributes(self):
        count = 0
        Attribute_Obj = self.env['product.attribute']
        for line in self.import_lines.filtered_domain([('executed', '=', False)]):
            if count < self.limit:
                line._process_attributes(Attribute_Obj)
                count += 1
                line.executed = True
            else:
                break
        if self.check_completed_execution():
            self.state = 'attribute'


class ProductSmartImportLine(models.Model):
    _name = 'product.smart.import.line'
    _description = 'Product Order Import Line'
    order = 'product_code'

    import_id = fields.Many2one('product.smart.import', ondelete='cascade')
    product_template_id = fields.Many2one('product.template', string='Plantilla Odoo',copy=False)
    product_id = fields.Many2one('product.product', string='Variante P. Odoo',copy=False)
    product_code = fields.Char('Cod. Producto',copy=False)
    product_name = fields.Char('Nombre',copy=False)
    category_name = fields.Char('Nombre Categoría',copy=False)
    size = fields.Char('Talla')
    size_2 = fields.Char('Tamaño')
    measure = fields.Char('Medida')
    color = fields.Char('Color')
    price = fields.Float('Precio')
    executed = fields.Boolean(readonly=1, string='Ejecutado')
    error = fields.Char()
    category_id = fields.Many2one('product.category', string='Categoría')

    def _create_category(self, Category_Obj):
        if self.category_name:
            categories = self.category_name.split('/')
            last_parent_id = False
            for categ in categories:
                category = Category_Obj.search([('name','=',categ.strip())],limit=1)
                if category:
                    if category.parent_id:
                        last_parent_id = category.id
                    else:
                        category.parent_id = last_parent_id
                        last_parent_id = category.id
                else:
                    last_parent_id = Category_Obj.create({'name': categ, 'parent_id': last_parent_id}).id
            self.category_id = last_parent_id

    def _process_attributes(self, Attribute_Obj):
        if self.measure:
            self._helper_create_attributes(Attribute_Obj, self.measure, "Medidas")
        if self.size:
            self._helper_create_attributes(Attribute_Obj, self.size, "Talla")
        if self.size_2:
            self._helper_create_attributes(Attribute_Obj, self.size_2, "Tamaño")
        if self.color:
            self._helper_create_attributes(Attribute_Obj, self.color, "Color")

    def _helper_create_attributes(self, Attribute_Obj,value_name, attribute_name):
        attribute = Attribute_Obj.search([('name', '=', attribute_name)], limit=1)
        if not attribute:
            attribute = Attribute_Obj.create({
                'name': attribute_name
            })
        value = attribute.value_ids.filtered_domain([('name', '=', value_name)])
        if not value:
            attribute.value_ids.create({'name': value_name, 'attribute_id': attribute.id})







#
#     def _helper_create_product.smart(self, SaleObj, SaleLineObj, ProductObj,PartnerObj):
#         if self.code_customer != 0:
#             partner_id = PartnerObj.search([('code_customer','=',self.code_customer),('active','in',[True,False])],limit=1)
#             if partner_id:
#                 vals = {
#                     'company_id': self.company_id.id,
#                     'partner_id': partner_id.id,
#                     'date_smart': self.date_smart,
#                     'name': self.smart_num,
#                     'old_id': self.smart_num,
#                     'global_amount': self.discount,
#                     'note': self.notes,
#                 }
#                 new_smart = SaleObj.create(vals)
#                 new_smart._onchange_partner_id()
#                 new_smart.onchange_partner_id()
#                 new_smart.onchange_partner_shipping_id()
#                 new_smart.onchange_cross_doc_classification()
#                 new_smart.cross_doc_classification = self.import_id.cross_doc_classification
#                 new_smart._onchange_partner_id_route()
#                 self.product.id = new_smart.id
#                 self.executed = True
#                 self._create_smart_lines(SaleObj,SaleLineObj, ProductObj)
#             else:
#                 self._register_not_partner_found()
#         else:
#             self._register_not_partner_found()
#
#     def _register_not_partner_found(self):
#         self.error = "No podemos buscar Contacto con código de Cliente %s"%self.code_customer
#
#     def _create_smart_lines(self, SaleObj,SaleLineObj, ProductObj):
#         for line in self.import_id.import_smart_lines.filtered_domain([('company', '=', self.company_id.id), ('product.id', '=', False),('smart_num', '=', self.smart_num)]):
#             line.create_product.line_from_import_line(SaleObj, SaleLineObj, ProductObj)
#
#     @api.depends('product.id','product.id.amount_total','product.id.amount_untaxed','product.id.amount_tax')
#     def _compute_migration_difference(self):
#         for line in self:
#             is_different = False
#             motive = ''
#             amount_taxed_diff = 0
#             amount_untaxed_diff = 0
#             amount_total_diff = 0
#             if line.product.id:
#                 difference = self.round_difference(line.product.id.amount_untaxed,line.amount_untaxed)
#                 if difference > line.import_id.difference_allowed:
#                     amount_untaxed_diff = difference
#                     is_different = True
#                     motive +='DIFERENCIA EN BASE IMPONIBLE - EN PEDIDO %s - EN IMPORTACIÓN %s\n'%(line.product.id.amount_untaxed,line.amount_untaxed)
#                 difference = self.round_difference(line.product.id.amount_tax,line.amount_taxed)
#                 if difference > line.import_id.difference_allowed:
#                     amount_taxed_diff = difference
#                     is_different = True
#                     motive +='DIFERENCIA TOTAL IMPUESTOS - EN PEDIDO %s - EN IMPORTACIÓN %s\n'%(line.product.id.amount_tax,line.amount_taxed)
#                 difference = self.round_difference(line.product.id.amount_total, line.amount_total)
#                 if difference > line.import_id.difference_allowed:
#                     amount_total_diff = difference
#                     is_different = True
#                     motive +='DIFERENCIA TOTAL PEDIDO EN PEDIDO %s - EN IMPORTACIÓN %s\n'%(line.product.id.amount_total, line.amount_total)
#                 if is_different:
#                     line.product.id.migration_difference = True
#                     line.product.id.migration_difference_motive = motive
#                 else:
#                     line.product.id.state = 'product.
#             line.migration_difference = is_different
#             line.amount_taxed_diff = amount_taxed_diff
#             line.amount_untaxed_diff = amount_untaxed_diff
#             line.amount_total_diff = amount_total_diff
#
#     def round_difference(self, smart_number, line_number):
#         difference = line_number - smart_number
#         if difference < 0:
#             difference = difference *-1
#         return difference
#
# class SaleLineImportLine(models.Model):
#     _name = 'product.smart.line.import.line'
#     _description = 'Sale Order Line Import Line'
#
#     import_id = fields.Many2one('product.smart.import', ondelete='cascade')
#     company_id = fields.Many2one('res.company',related='import_id.company_id')
#     company = fields.Integer('Empresa')
#     product.id = fields.Many2one('product.smart', string='Venta Odoo',related='product.line_id.smart_id')
#     product.line_id = fields.Many2one('product.smart.line',copy=False)
#     smart_num = fields.Integer('Núm. Orden')
#     picking_num = fields.Integer('Albarán')
#     sequence = fields.Integer('Secuencia')
#     default_code = fields.Char('Código Barra')
#     product_uom_qty = fields.Float('Cantidad')
#     price = fields.Float('Precio')
#     discount = fields.Float('Descuento')
#     iva = fields.Char('Iva')
#     description = fields.Char('Descripción')
#     box_qty = fields.Integer('Cajas')
#     cost = fields.Float('Coste')
#     old_id = fields.Integer('Id')
#     executed = fields.Boolean('Ejecutado',copy=False)
#     error = fields.Char(default='',copy=False)
#
#     def create_product.line_from_import_line(self, SaleObj,SaleLineObj, ProductObj):
#         possible_smart_line = SaleLineObj.search([('old_id','=',self.old_id)],limit=1)
#         if possible_smart_line:
#             self.product.line_id = possible_smart_line.id
#         else:
#             self._helper_create_product.smart_line(SaleObj,SaleLineObj, ProductObj)
#
#     def _helper_create_product.smart_line(self, SaleObj,SaleLineObj, ProductObj):
#         smart_id = SaleObj.search([('old_id','=',self.smart_num),('company_id','=',self.company_id.id)],limit=1)
#         vals = {}
#         if smart_id:
#             vals.update({'smart_id': smart_id.id})
#             product_id = False
#             if self.default_code != 0:
#                 product_id = ProductObj.search([('barcode','=','0%s'%self.default_code),('active','in',[True,False])],limit=1) or False
#             if not product_id:
#                 product_id = self.import_id.generic_product_id
#             vals = {
#                 'company_id': self.company_id.id,
#                 'smart_id': smart_id.id,
#                 'product_id': product_id.id,
#                 'name': self.description,
#                 'migrated_picking_id': self.picking_num,
#                 'price_unit': self.price,
#                 'discount': self.discount,
#                 'product_standard_price': self.cost,
#                 'box_qty': self.box_qty,
#                 'old_id': self.id,
#                 'product_uom': product_id.uom_id.id,
#                 'product_uom_qty': self.product_uom_qty,
#             }
#             taxes = self._find_iva_to_migrate(str(self.iva),smart_id)
#             if taxes:
#                 vals.update({'tax_id': [(6,0, taxes)]})
#             else:
#                 vals.update({'tax_id': []})
#             new_smart_line = SaleLineObj.create(vals)
#             new_smart_line.onchange_discount_price_unit_for_best_price()
#             new_smart_line.onchange_best_price_price_unit_for_discount()
#             self.product.line_id = new_smart_line.id
#             self.executed = True
#         else:
#             self._register_not_smart_found()
#
#     def _register_not_smart_found(self):
#         self.error = "No encontramos Pedido %s" % self.smart_num
#
#     def _find_iva_to_migrate(self, iva, smart_id):
#         tax = self.env['account.tax'].search(
#             [('type_tax_use', '=', 'product.), ('migration_label', '=', iva), ('company_id', '=', self.company_id.id)],
#             limit=1)
#         taxes = False
#         if tax:
#             taxes = []
#             taxes.append(tax.id)
#             if smart_id.fiscal_position_id and smart_id.fiscal_position_id.tax_ids:
#                 for tax_line in smart_id.fiscal_position_id.tax_ids.filtered_domain([('tax_src_id', '=', tax.id)]):
#                     taxes.append(tax_line.tax_dest_id.id)
#         return taxes
#


