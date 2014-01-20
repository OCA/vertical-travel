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

import openerp.addons.decimal_precision as dp


class travel_service_rental(orm.Model):
    _description = _('Service rentals for travel')
    _name = 'travel.service.rental'

    _columns = {
        # TODO: hotel/other support
        'location': fields.many2one('res.partner', 'Location', required=True,
                                    help='Location of rental supplier.'),
        'country_id': fields.related('city_id', 'country_id', type='many2one',
                                     relation='res.country', string="Country",
                                     readonly=True, help='Country of rental.'),
        'city_id': fields.many2one('res.better.zip', 'City', required='True',
                                   help='City of rental.'),
        'start': fields.datetime('Start', required=True,
                                 help='Start date and time of rental.'),
        'end': fields.datetime('End', required=True,
                               help='End date and time of rental.'),
        'capacity': fields.integer('Capacity', help='Maximum capacity of people in room.'),
        'equipment': fields.text('Desired equipment'),
        'services': fields.text('Desired services'),
        'passenger_id': fields.many2one('travel.passenger', 'Passenger', required=True,
                                        help='Passenger of this rental.'),

    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
