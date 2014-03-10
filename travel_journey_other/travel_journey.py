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
        'other_from': fields.char('Origin'),
        'other_to': fields.char('Destination'),
        'other_departure': fields.datetime(
            'Departure', help='Date and time of the  departure of the special '
                              'transportation type.'),
        'other_arrival': fields.datetime(
            'Arrival', help='Date and time of the arrival of the special '
                            'transportation type.'),
        'other_capacity': fields.integer(
            'Capacity', help='Number of passengers who can take this mode of '
                             'transport'),
        'other_description': fields.text('Description'),
    }

    def init(self, cr):
        """Register this class to be able to do polymorphic things"""
        self._journey_type_classes['other'] = travel_journey

    def _estimate_typed_date(self, journey, field_name):
        """If there is a start date from flight, use it"""
        if field_name == 'date_start':
            return journey.other_departure
        elif field_name == 'date_stop':
            return journey.other_arrival

    def _inv_estimate_typed_date(self, journey, field_name, val):
        """If there is no start date in flight, set it in base"""
        if field_name == 'date_start' and journey.other_departure:
            journey.write({'other_departure': val})
        elif field_name == 'date_stop' and journey.other_arrival:
            journey.write({'other_arrival': val})
        else:
            return False
        return True
