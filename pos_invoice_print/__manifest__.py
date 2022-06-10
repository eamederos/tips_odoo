##############################################################################
#
#
##############################################################################

{
    'name': 'POS Invoice Print',
    'version': '14.0.1.0.0',
    'author': 'Ernesto Mederos',
    'maintainer': 'Ernesto Mederos',
    'website': 'http://www.ynext.cl',
    'license': 'AGPL-3',
    'category': 'Point of Sale',
    'summary': 'Impresión de Facturas.',
    'depends': ['point_of_sale'],
    'data': [
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'images': ['static/description/banner.jpg'],
}
