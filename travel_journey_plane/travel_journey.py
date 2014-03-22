# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Savoir-faire Linux
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


class travel_journey(orm.Model):
    _inherit = 'travel.journey'
    _columns = {
        'airline': fields.many2one(
            'res.partner', 'Airline', domain="[('airline','=',True)]",
            help="Airline company."),
        'airport_from': fields.many2one(
            'res.partner', 'Origin', domain="[('airport','=',True)]",
            help="Departure airport."),
        'airport_to': fields.many2one(
            'res.partner', 'Destination', domain="[('airport','=',True)]",
            help="Destination airport."),
        'terminal_from': fields.char(
            'Terminal (origin)',
            help="Terminal number at departure airport"),
        'terminal_to': fields.char(
            'Terminal (destination)',
            help="Terminal number at destination airport"),
        'fight_departure': fields.datetime(
            'Flight Departure',
            help='Date and time of the departure of the flight.'),
        'fight_arrival': fields.datetime(
            'Flight Arrival',
            help='Date and time of the arrival of the flight.'),
    }

    def init(self, cr):
        """Register this class to be able to do polymorphic things"""
        self._journey_type_classes['plane'] = travel_journey

    def _estimate_typed_date(self, journey, field_name):
        """If there is a start date from flight, use it"""
        if field_name == 'date_start':
            return journey.fight_departure
        elif field_name == 'date_stop':
            return journey.fight_arrival

    def _inv_estimate_typed_date(self, journey, field_name, val):
        """If there is no start date in flight, set it in base"""
        if field_name == 'date_start' and journey.fight_departure:
            journey.write({'fight_departure': val})
        elif field_name == 'date_stop' and journey.fight_arrival:
            journey.write({'fight_arrival': val})
        else:
            return False
        return True

    def _company_typed_get(self, journey):
        return journey.airline.name_get()[0][1]
