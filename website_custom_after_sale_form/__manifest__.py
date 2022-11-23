##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Website After Sale Custom Form',
    'version': '14.0.1.0.0',
    'author': 'Ynext SpA',
    'maintainer': 'Personal',
    'website': 'None',
    'license': 'AGPL-3',
    'category': 'Website',
    'summary': 'Module to create a custom form in website.',
    'depends': ['base','website'],
    'data': [
        'static/src/xml/custom_request_form.xml',
        'views/assets.xml'
    ],
    'images': ['static/description/banner.jpg'],
}
