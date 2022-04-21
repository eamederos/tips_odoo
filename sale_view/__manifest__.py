# coding: utf-8
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

{
    'name': 'Sale View',
    'version': '14.0.1.0.0',
    'author': 'Ernesto Mederos',
    'category': 'Base',
    'summary': 'Sale View',
    'depends': ['sale_management'],
    'data': [
        'views/assets.xml',
        'views/sale_view.xml',
    ],
    'qweb': [
        'static/src/xml/template.xml'
    ],
    'installable': True,
    'application': True,
    'demo': [],
    'test': []
}
