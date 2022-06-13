##############################################################################
#
##############################################################################

{
    'name': 'Purchase Custom Report',
    'version': '14.0.1.0.0',
    'author': 'Ernesto Mederos',
    'maintainer': 'Ernesto Mederos',
    'category': 'Point of Sale',
    'summary': 'Personalizar reporte de Compras.',
    'depends': ['purchase'],
    'data': [
        'report/purchase_quotation_report.xml',
        'report/purchase_order_report.xml',
    ],
    'qweb': [],
    'images': ['static/description/banner.jpg'],
}
