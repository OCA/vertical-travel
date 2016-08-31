
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2010 - 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
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

from openerp.osv import fields, orm
from openerp.addons.travel.res_config import (
    get_alert_address, DEFAULT_ALERT_ADDRESS
)


class travel_configuration(orm.TransientModel):
    _inherit = 'travel.config.settings'
    _columns = {
        'opened_alert_address': fields.char(
            'Travel PO Open Alert',
            help='E-mail address to send alert when a purchase order linked '
                 'to travel is opened.')
    }

    def get_default_opened_alert_address(self, cr, uid, ids, context=None):
        context = context or {}

        ctx = dict(context, alert_type='sent')
        return {
            'opened_alert_address': get_alert_address(
                self.pool.get("ir.config_parameter"), cr, uid, context=ctx)
        }

    def set_opened_alert_address(self, cr, uid, ids, context=None):
        context = context or {}

        if type(ids) is not list:
            ids = [ids]
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(
                cr, uid, "travel.opened_alert_address",
                record.opened_alert_address or DEFAULT_ALERT_ADDRESS,
                context=context)
