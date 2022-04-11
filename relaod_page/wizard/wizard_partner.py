#-*- coding: utf-8 -*-
import pandas
import logging
import os
import xlrd
import csv
import tempfile
import base64
from odoo.exceptions import UserError
from odoo import api, fields, models, _, SUPERUSER_ID
from datetime import datetime, timedelta, date

_logger = logging.getLogger(__name__)

class WizardPartner(models.TransientModel):
    _name = "wizard.partner"

    partner_text = fields.Text()
    partner_id = fields.Many2one('res.partner')

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        partner_id = self._context.get('active_id')
        res.update({
            'partner_id': partner_id
        })
        return res

    def action_update(self):
        self.partner_id.message_post(body=self.partner_text)
        return {'type': 'ir.actions.client', 'tag': 'reload'}