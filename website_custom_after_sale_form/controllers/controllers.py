import jinja2
from odoo import http
import logging
_logger = logging.getLogger(__name__)
from odoo.http import request
loader = jinja2.PackageLoader('odoo.addons.master_credit_base', 'views/web')
env = jinja2.Environment(loader=loader, autoescape=True)


class Master(http.Controller):

    @http.route(['/after_sale_form'], type='http', auth="public", website=True)
    def partner_form(self, **post):
        return request.render("website_custom_after_sale_form.after_sale_form", {})

    @http.route(['/after_sale_form/submit'], type='http', auth="public", website=True)
    def partner_info_form_submit(self, **post):
        pass


