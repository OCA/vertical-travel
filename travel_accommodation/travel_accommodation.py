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
from openerp.tools import (
    DEFAULT_SERVER_DATETIME_FORMAT,
    DEFAULT_SERVER_DATE_FORMAT,
)

from datetime import datetime

import openerp.addons.decimal_precision as dp


class travel_accommodation(orm.Model):

    """Accommodation of travel"""
    _description = _(__doc__)
    _name = 'travel.accommodation'
    _rec_name = 'location'

    @staticmethod
    def str_to_date_difference(lhs, rhs):
        def str_to_date(string):
            try:
                return datetime.strptime(
                    string, DEFAULT_SERVER_DATETIME_FORMAT
                ).date()
            except ValueError:
                return datetime.strptime(
                    string, DEFAULT_SERVER_DATE_FORMAT
                ).date()
        return (str_to_date(lhs) - str_to_date(rhs)).days

    @staticmethod
    def _check_dep_arr_dates(departure, arrival):
        return not departure or not arrival or departure <= arrival

    def on_change_times(self, cr, uid, ids, arrival, departure, context=None):
        if arrival and departure:
            nights = self.str_to_date_difference(departure, arrival)
            if nights >= 0:
                return {'value': {'nights': nights}}
            return {
                'value': {
                    'departure': False,
                    'nights': False,
                },
                'warning': {
                    'title': _('Arrival after Departure'),
                    'message': _('Departure (%s) cannot be before '
                                 'Arrival (%s).') % (departure, arrival),
                },
            }
        return {}

    def _get_nights(self, cr, uid, ids, fieldnames, args, context=None):
        return {obj.id: self.str_to_date_difference(obj.departure, obj.arrival)
                for obj in self.browse(cr, uid, ids, context=context)}

    def check_date(self, cr, uid, ids, context=None):
        if not ids:
            return False
        accommodation = self.browse(cr, uid, ids[0], context=context)
        return not self._check_dep_arr_dates(accommodation.departure,
                                             accommodation.arrival)

    def check_currency(self, cr, uid, ids, context=None):
        if not ids:
            return False
        accommodation = self.browse(cr, uid, ids[0], context=context)
        return not (bool(accommodation.budget) ^
                    bool(accommodation.budget_currency))

    _columns = {
        'location': fields.many2one('res.partner', 'Location',
                                    help='Location of Accommodation.'),
        'close_to': fields.char(
            'Close to', help='Location in proximity to Accommodations.'),
        'budget': fields.float(
            'Budget per Night',
            digits_compute=dp.get_precision('Product Price'),
            help='Budget to allocate per night spent at Accommodations.'),
        'budget_currency': fields.many2one(
            'res.currency', 'Currency of budget', help='Currency of budget.'),
        'arrival': fields.datetime(
            'Arrival', required=True,
            help='Date and Time of arrival at Accommodations.'),
        'departure': fields.datetime(
            'Departure', required=True,
            help='Date and Time of departure from Accommodations.'),
        'nights': fields.function(_get_nights, string='Nights', type='float',
                                  digits=(1, 0)),
        'breakfast': fields.boolean(
            'Breakfast',
            help='Is breakfast included?',
        ),
        'lunch': fields.boolean('Lunch', help='Is lunch included?'),
        'dinner': fields.boolean('Dinner', help='Is dinner included?'),
        'passenger_id': fields.many2one(
            'travel.passenger', 'Passenger', required=True,
            help='Passenger on this accommodation.'),

    }

    _constraints = [
        (check_date,
         _('Arrival date cannot be after departure date.'),
         ['departure', 'arrival']),
        (check_currency,
         _('Currency not specified for budget.'),
         ['budget', 'budget_currency', ])
    ]
