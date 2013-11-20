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
from datetime import datetime

import openerp.addons.decimal_precision as dp


class travel_car_rental(orm.Model):
    _description = 'Car Rentals for travel'
    _name = 'travel.car.rental'

    _columns = {
        'pickup_loc': fields.char('Pick-up Location', size=255, help="Location of car pick-up."),
        'dropoff_loc': fields.char('Drop-off Location', size=255, help="Location of car drop-off."),
        'type': fields.char('Vehicle type', size=255, help="Make and model of the car."),
        'start': fields.datetime('Start', required=True,
                                 help='Start date and time of car rental.'),
        'end': fields.datetime('End', required=True,
                               help='End date and time of car rental.'),
        'driver': fields.boolean('With Chauffeur', help='Will the car rental require a driver.'),
        'passenger_id': fields.many2one('travel.passenger', 'Passenger', required=True,
                                        help='Passenger on this accommodation.'),

    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
