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


class travel_accommodation(orm.Model):
    _description = 'Accommodation of travel'
    _name = 'travel.accommodation'

    def _get_nights(self, cr, uid, ids, fieldnames, args, context=None):
        def str_to_date(string):
            return datetime.strptime(string, '%Y-%m-%d').date()

        return {obj.id: (str_to_date(obj.arrival) - str_to_date(obj.departure)).days
                for obj in self.browse(cr, uid, ids, context=context)}

    _columns = {
        # TODO: hotel/other support
        'location': fields.many2one('res.partner', 'Location', required=True,
                                    help='Location of Accommodation.'),
        'close_to': fields.char('Close to', size=256,
                                help='Location in proximity to Accommodations.'),
        'budget': fields.float('Budget per Night', digits_compute=dp.get_precision('Product Price'),
                               help='Budget to allocate per night spent at Accommodations.'),
        'arrival': fields.date('Arrival', required=True,
                               help='Date of arrival at Accommodations.'),
        'departure': fields.date('Departure', required=True,
                                 help='Date of departure from Accommodations.'),
        # TODO: calculate next when previous two are changed
        'nights': fields.function(_get_nights, string='Nights', type='float'),
        'breakfast': fields.boolean('Breakfast', help='Is breakfast included?'),
        'lunch': fields.boolean('Lunch', help='Is lunch included?'),
        'dinner': fields.boolean('Dinner', help='Is dinner included?'),
        'passenger_id': fields.many2one('travel.passenger', 'Passenger', required=True,
                                        help='Passenger on this accommodation.'),

    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
