##############################################################################
#
#    OpenERP, Open Source Management Solution
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Product Smart Import',
    'version': '14.0.1.0.0',
    'author': 'Ernesto A. Mederos',
    'maintainer': 'Ernesto A. Mederos',
    'license': 'AGPL-3',
    'category': 'Extra Tools',
    'summary': 'Product Smart Import',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        # 'data/ir_cron.xml',
        'views/product_smart_import_view.xml',
        'views/menu.xml',
    ],
    'images': ['static/description/banner.jpg'],
}
