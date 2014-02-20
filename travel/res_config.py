# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
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


def get_basic_passenger_limit(ir_config_parameter_pool, cr, uid, context=None):
    try:
        limit = ir_config_parameter_pool.get_param(
            cr, uid, "travel.basic_passenger_limit", context=context)
        limit = int(limit) or DEFAULT_PASSENGER_LIMIT
    except (ValueError, TypeError, AttributeError):
        limit = DEFAULT_PASSENGER_LIMIT
    finally:
        return limit


class travel_configuration(orm.TransientModel):
    _name = 'travel.config.settings'
    _inherit = 'res.config.settings'
    _columns = {
        'basic_passenger_limit': fields.integer(
            'Basic Passenger Limit',
            help='Limit number of passengers to organize travels by '
                 'non-managers.'),
    }

    def get_default_basic_passenger_limit(self, cr, uid, ids, context=None):
        return {
            'basic_passenger_limit': get_basic_passenger_limit(
                self.pool.get("ir.config_parameter"), cr, uid, context=context)
        }

    def set_basic_passenger_limit(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(
                cr, uid, "travel.basic_passenger_limit",
                record.basic_passenger_limit or DEFAULT_PASSENGER_LIMIT,
                context=context)
