# -*- encoding: utf-8 -*-
# #############################################################################
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
from openerp.tools.translate import _


class travel_journey_order_form(orm.TransientModel):
    _name = "travel.journey.order.form"
    _description = "Travel Journey Order Form"
    _columns = {
        'travel_id': fields.many2one(
            'travel.travel', string="Travel", required=True),
        'journey_id': fields.many2one(
            'travel.journey', string="Journey", required=True),
    }

    def print_report(self, cr, uid, ids, data, context=None):
        wizard = self.browse(cr, uid, ids, context=context)[0]
        journey = wizard.journey_id
        data['ids'] = [journey.id]
        data['model'] = ['travel.journey']

        # Check if the passenger of the journey is related to a hr.employee
        # if not the report cannot be generated as it requires details
        # from employee.
        # It seems logically it should not happen, but as the system allows
        # it, we prefer to inform the user how to fix the issue.
        user_object = self.pool['res.users']
        employee_object = self.pool['hr.employee']
        passenger_name = journey.passenger_id.partner_id.name or ''
        partner_id = journey.passenger_id.partner_id.id
        user_ids = user_object.search(
            cr, uid, [('partner_id', '=', partner_id)])
        employee_ids = employee_object.search(
            cr, uid, [('user_id', 'in', user_ids)])

        if not employee_ids:
            raise orm.except_orm(
                _('Error'),
                _(
                    'The passenger "%s" is not linked to any employee. '
                    'The report cannot be generated.'
                ) % passenger_name
            )

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'travel.journey.order.webkit',
            'datas': data,
        }

    def update_journey_domain(self, cr, uid, ids, travel_id, context=None):
        travel_pool = self.pool.get('travel.travel')
        travel = travel_pool.browse(cr, uid, travel_id, context=context)
        return {
            'domain': {
                'budgets': [('id', 'in', [j.id for j in travel.journey_ids])],
            }
        }


'airline'
'airport_from'
'airport_to'
'arrival'
'baggage_qty'
'baggage_weight'
'baggage_weight_uom'
'cancellation'
'class_id'
'comment'
'date_start'
'date_stop'
'departure'
'destination'
'fight_arrival'
'fight_departure'
'is_return'
'origin'
'other_arrival'
'other_capacity'
'other_departure'
'other_description'
'other_from'
'other_to'
'passenger_function'
'passenger_function_ids'
'passenger_id'
'product_uom_categ_kgm_ref'
'railway_company'
'railway_station_arrival'
'railway_station_departure'
'railway_station_from'
'railway_station_to'
'reservation'
'return_arrival'
'return_departure'
'return_destination'
'return_origin'
'state'
'terminal_from'
'terminal_to'
'travel'
'type'
