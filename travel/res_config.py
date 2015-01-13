
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

DEFAULT_PASSENGER_LIMIT = 10
DEFAULT_ALERT_ADDRESS = 'root@localhost'


def get_basic_passenger_limit(ir_config_parameter_pool, cr, uid, context=None):
    try:
        limit = ir_config_parameter_pool.get_param(
            cr, uid, "travel.basic_passenger_limit", context=context)
        limit = int(limit) or DEFAULT_PASSENGER_LIMIT
    except (ValueError, TypeError, AttributeError):  # pragma: no cover
        limit = DEFAULT_PASSENGER_LIMIT
    finally:
        return limit


def get_alert_address(ir_config_parameter_pool, cr, uid, context=None):
    context = context or {}

    if 'alert_type' in context:
        if context['alert_type'] == 'sent':
            address_field = 'travel.sent_alert_address'
        elif context['alert_type'] == 'reserved':
            address_field = 'travel.reserved_alert_address'
        elif context['alert_type'] == 'opened':
            address_field = 'travel.opened_alert_address'

    try:
        address = ir_config_parameter_pool.get_param(
            cr, uid, address_field, context=context)
    except (ValueError, TypeError, AttributeError):  # pragma: no cover
        address = DEFAULT_ALERT_ADDRESS
    finally:
        return address


class travel_configuration(orm.TransientModel):
    _name = 'travel.config.settings'
    _inherit = 'res.config.settings'
    _columns = {
        'basic_passenger_limit': fields.integer(
            'Basic Passenger Limit',
            help='Limit number of passengers to organize travels by '
                 'non-managers.'),
        'sent_alert_address': fields.char(
            'Travel Sent Alert',
            help='E-mail address to send alert when a travel is '
                 'send to the travel office.')
    }

    def get_default_basic_passenger_limit(self, cr, uid, ids, context=None):
        return {
            'basic_passenger_limit': get_basic_passenger_limit(
                self.pool.get("ir.config_parameter"), cr, uid, context=context)
        }

    def set_basic_passenger_limit(self, cr, uid, ids, context=None):
        if type(ids) is not list:
            ids = [ids]
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(
                cr, uid, "travel.basic_passenger_limit",
                record.basic_passenger_limit or DEFAULT_PASSENGER_LIMIT,
                context=context)

    def get_default_sent_alert_address(self, cr, uid, ids, context=None):
        context = context or {}

        ctx = dict(context, alert_type='sent')
        return {
            'sent_alert_address': get_alert_address(
                self.pool.get("ir.config_parameter"), cr, uid, context=ctx)
        }

    def set_sent_alert_address(self, cr, uid, ids, context=None):
        context = context or {}

        if type(ids) is not list:
            ids = [ids]
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(
                cr, uid, "travel.sent_alert_address",
                record.sent_alert_address or DEFAULT_ALERT_ADDRESS,
                context=context)
