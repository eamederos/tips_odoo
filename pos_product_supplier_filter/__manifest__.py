##############################################################################
#
##############################################################################

{
    'name': 'POS Product Supplier Filter MFH',
    'version': '14.0.1.0.0',
    'author': 'Ernesto Mederos',
    'maintainer': 'Ernesto Mederos',
    'category': 'Point of Sale',
    'summary': 'Búsqueda proveedor Venta.',
    'depends': ['point_of_sale','purchase'],
    'data': [
        'views/res_partner_views.xml',
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/SupplierFilter.xml',
        'static/src/xml/Chrome.xml',
    ],
    'images': ['static/description/banner.jpg'],
}
