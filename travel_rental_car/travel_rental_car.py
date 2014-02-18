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
from openerp.tools.translate import _


class travel_car_rental(orm.Model):
    """Car Rentals for travel"""
    _name = 'travel.rental.car'
    _description = _(__doc__)

    @staticmethod
    def _check_dep_arr_dates(start, end):
        return not start or not end or start <= end

    def on_change_times(self, cr, uid, ids, start, end, context=None):
        if self._check_dep_arr_dates(start, end):
            return {}
        return {
            'value': {
                'end': False,
            },
            'warning': {
                'title': 'Arrival after Departure',
                'message': ('End of rental (%s) cannot be before Start (%s).' %
                            (start, end)),
            },
        }

    def check_date(self, cr, uid, ids, context=None):
        if not ids:
            return False
        rental = self.browse(cr, uid, ids[0], context=context)
        return self._check_dep_arr_dates(rental.start, rental.end)

    _columns = {
        'pickup_loc': fields.char('Pick-up Location',
                                  help="Location of car pick-up."),
        'dropoff_loc': fields.char('Drop-off Location',
                                   help="Location of car drop-off."),
        'type': fields.many2one('vehicle.vehicle', 'Vehicle type',
                                help="Make and model of the car."),
        'start': fields.datetime('Start', required=True,
                                 help='Start date and time of car rental.'),
        'end': fields.datetime('End', required=True,
                               help='End date and time of car rental.'),
        'driver': fields.boolean('With Chauffeur',
                                 help='Will the car rental require a driver.'),
        'passenger_id': fields.many2one('travel.passenger', 'Passenger',
                                        required=True,
                                        help='Passenger on this car rental.'),
    }

    _constraints = [
        (check_date, 'End date cannot be after Start date.', ['start', 'end']),
    ]
