# coding: utf-8
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

{
    'name': 'Reload Page',
    'version': '14.0.1.0.0',
    'author': 'Ernesto Mederos',
    'category': 'Base',
    'summary': 'Escribir en el chatter y recargar página del contacto',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard_partner.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'application': True,
    'demo': [],
    'test': []
}
