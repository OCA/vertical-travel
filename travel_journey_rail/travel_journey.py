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
        'railway_company': fields.many2one(
            'res.partner', 'Railway Company',
            domain="[('railway_company','=',True)]", help="Railway Company."),
        'railway_station_from': fields.many2one(
            'res.partner', 'Origin', domain="[('railway_station','=',True)]",
            help="Departure Railway Station."),
        'railway_station_to': fields.many2one(
            'res.partner', 'Destination',
            domain="[('railway_station','=',True)]",
            help="Destination Railway Station."),
        'railway_station_departure': fields.datetime(
            'Departure', help='Date and time of the departure of the train.'),
        'railway_station_arrival': fields.datetime(
            'Arrival', help='Date and time of the arrival of the train.'),
    }

    def init(self, cr):
        """Register this class to be able to do polymorphic things"""
        self._journey_type_classes['rail'] = travel_journey

    def _estimate_typed_date(self, journey, field_name):
        """If there is a start date from flight, use it"""
        if field_name == 'date_start':
            return journey.railway_station_departure
        elif field_name == 'date_stop':
            return journey.railway_station_arrival

    def _inv_estimate_typed_date(self, journey, field_name, val):
        """If there is no start date in flight, set it in base"""
        if (field_name == 'date_start' and
                journey.railway_station_departure):
            journey.write({'railway_station_departure': val})
        elif (field_name == 'date_stop' and
                journey.railway_station_arrival):
            journey.write({'railway_station_arrival': val})
        else:
            return False
        return True

