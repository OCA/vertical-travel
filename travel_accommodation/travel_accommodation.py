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
from datetime import datetime

import openerp.addons.decimal_precision as dp


class travel_accommodation(orm.Model):
    _description = _('Accommodation of travel')
    _name = 'travel.accommodation'

    @staticmethod
    def str_to_date_difference(lhs, rhs):
        def str_to_date(string):
            return datetime.strptime(string, '%Y-%m-%d %H:%M:%S').date()
        return (str_to_date(lhs) - str_to_date(rhs)).days

    def on_change_times(self, cr, uid, ids, arrival, departure, context=None):
        nights = 0
        if arrival and departure:
            nights = self.str_to_date_difference(departure, arrival)
        return {'value': {'nights': nights}}

    def _get_nights(self, cr, uid, ids, fieldnames, args, context=None):
        return {obj.id: self.str_to_date_difference(obj.departure, obj.arrival)
                for obj in self.browse(cr, uid, ids, context=context)}

    _columns = {
        # TODO: hotel/other support
        'location': fields.many2one('res.partner', 'Location', required=True,
                                    help='Location of Accommodation.'),
        'close_to': fields.char('Close to', size=256,
                                help='Location in proximity to Accommodations.'),
        'budget': fields.float('Budget per Night', digits_compute=dp.get_precision('Product Price'),
                               help='Budget to allocate per night spent at Accommodations.'),
        'arrival': fields.datetime(
            'Arrival', required=True,
            help='Date and Time of arrival at Accommodations.'),
        'departure': fields.datetime(
            'Departure', required=True,
            help='Date and Time of departure from Accommodations.'),
        # TODO: calculate next when previous two are changed
        'nights': fields.function(_get_nights, string='Nights', type='float', digits=(1, 0)),
        'breakfast': fields.boolean('Breakfast', help='Is breakfast included?'),
        'lunch': fields.boolean('Lunch', help='Is lunch included?'),
        'dinner': fields.boolean('Dinner', help='Is dinner included?'),
        'passenger_id': fields.many2one('travel.passenger', 'Passenger', required=True,
                                        help='Passenger on this accommodation.'),

    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
