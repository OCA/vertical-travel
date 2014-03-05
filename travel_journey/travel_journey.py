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
import logging
_logger = logging.getLogger(__name__)


class travel_journey(orm.Model):
    """Journey of travel"""
    _name = 'travel.journey'
    _description = _(__doc__)
    _journey_type_classes = {}

    @staticmethod
    def _check_dep_arr_dates(departure, arrival):
        return not departure or not arrival or departure <= arrival

    def _gantt_date(self, cr, uid, ids, field_name, arg, context=None):
        """If there is no start date from journey, get it from travel"""
        if type(ids) in (int, long):
            ids = [ids]
        res = {}
        for journey in self.browse(cr, uid, ids, context=context):
            date = False
            if journey.type:
                try:
                    journey_class = self._journey_type_classes[journey.type]
                    date = journey_class._gantt_typed_date(
                        self, journey, field_name)
                except KeyError:
                    _logger.error(
                        _('Transportation type "%s" has not registered its '
                          'class in _journey_types, skipping its dates')
                        % journey.type)
                except AttributeError:
                    _logger.error(
                        _('Transportation type "%s" has not registered a '
                          '_gatt_typed_date() function, skipping its dates')
                        % journey.type)
            if field_name == 'gantt_date_start':
                date = (date or journey.departure or
                        journey.passenger_id.travel_id.date_start)
            elif field_name == 'gantt_date_stop':
                date = (date or journey.arrival or
                        journey.passenger_id.travel_id.date_stop)
            res[journey.id] = date
        return res

    def _inv_gantt_date(self, cr, uid, ids, field_name, val, arg, context=None):
        """If there is no start date in journey, set it in travel"""
        if type(ids) in (int, long):
            ids = [ids]
        for journey in self.browse(cr, uid, ids, context=context):
            if journey.type:
                try:
                    journey_class = self._journey_type_classes[journey.type]
                    if (journey_class._inv_gantt_typed_date(
                            self, journey, field_name, val)):
                        continue
                except KeyError:
                    _logger.error(
                        _('Transportation type "%s" has not registered its '
                          'class in _journey_types, skipping its dates')
                        % journey.type)
                except AttributeError:
                    _logger.error(
                        _('Transportation type "%s" has not registered a '
                          '_inv_gantt_typed_date() function, skipping its '
                          'dates') % journey.type)
            if field_name == 'gantt_date_start':
                if journey.departure:
                    journey.write({'departure': val})
                elif journey.passenger_id.travel_id.date_start:
                    journey.passenger_id.travel_id.write({'date_start': val})
            elif field_name == 'gantt_date_stop':
                if journey.arrival:
                    journey.write({'arrival': val})
                elif journey.passenger_id.travel_id.date_stop:
                    journey.passenger_id.travel_id.write({'date_stop': val})

    def _default_class(self, cr, uid, context=None):
        ir_model_data = self.pool.get('ir.model.data')
        return ir_model_data.get_object_reference(
            cr, uid, 'travel_journey', 'travel_journey_class_directive',)[1]

    def _get_type(self, cr, uid, context=None):
        acc_type_obj = self.pool.get('travel.journey.type')
        ids = acc_type_obj.search(cr, uid, [])
        res = acc_type_obj.read(cr, uid, ids, ['code', 'name'], context)
        return [(r['code'], r['name']) for r in res]

    def create(self, cr, uid, vals, context=None):
        """If is_return is checked, create a return trip after."""
        def clear_return_vals(mVals):
            mVals = mVals.copy()
            if mVals['is_return']:
                mVals['is_return'] = False
                mVals['return_origin'] = False
                mVals['return_destination'] = False
                mVals['return_departure'] = False
                mVals['return_arrival'] = False
            return mVals
        return_vals = None
        if vals['is_return']:
            return_vals = clear_return_vals(vals.copy())
            return_vals['is_return'] = False
            return_vals['origin'] = vals['destination']
            return_vals['destination'] = vals['origin']
            return_vals['departure'] = vals['return_departure']
            return_vals['arrival'] = vals['return_arrival']
        vals = clear_return_vals(vals)
        res = super(travel_journey, self).create(cr, uid, vals, context=context)
        if return_vals:
            super(travel_journey, self).create(cr, uid, return_vals,
                                               context=context)
        return res

    @staticmethod
    def on_change_return(cr, uid, ids, key, location, context=None):
        return {'value': {key: location}}

    def on_change_times(self, cr, uid, ids, departure, arrival,
                        return_trip=False, context=None):
        if self._check_dep_arr_dates(departure, arrival):
            return {}
        return {
            'value': {
                'return_arrival' if return_trip else 'arrival': False,
            },
            'warning': {
                'title': 'Arrival after Departure',
                'message': ('Departure (%s) cannot be before Arrival (%s).' %
                            (departure, arrival)),
            },
        }

    def check_date_exists(self, cr, uid, ids, context=None):
        if not ids:
            return False
        journey = self.browse(cr, uid, ids[0], context=context)
        return journey.departure or journey.arrival

    def check_date_exists_return(self, cr, uid, ids, context=None):
        if not ids:
            return False
        journey = self.browse(cr, uid, ids[0], context=context)
        return (not journey.is_return or
                journey.return_departure or journey.return_arrival)

    def check_date(self, cr, uid, ids, context=None):
        if not ids:
            return False
        journey = self.browse(cr, uid, ids[0], context=context)
        return self._check_dep_arr_dates(journey.departure, journey.arrival)

    def check_date_return(self, cr, uid, ids, context=None):
        if not ids:
            return False
        journey = self.browse(cr, uid, ids[0], context=context)
        return self._check_dep_arr_dates(journey.return_departure,
                                         journey.return_arrival)

    def check_uom(self, cr, uid, ids, context=None):
        if not ids:
            return False
        journey = self.browse(cr, uid, ids[0], context=context)
        return not (bool(journey.baggage_weight) ^
                    bool(journey.baggage_weight_uom))

    def name_get(self, cr, uid, ids, context=None):
        return [
            (journey.id,
             "%s (%s -> %s)" % (journey.passenger_id.partner_id.name,
                                journey.origin.name_get()[0][1],
                                journey.destination.name_get()[0][1]))
            for journey in self.browse(cr, uid, ids, context=context)
        ]

    _columns = {
        'origin': fields.many2one(
            'res.better.zip', 'Origin', required='True',
            help='Source city of travel.'),
        'destination': fields.many2one(
            'res.better.zip', 'Destination', required='True',
            help='Destination city of travel.'),
        'return_origin': fields.many2one('res.better.zip', 'Origin (return)'),
        'return_destination': fields.many2one(
            'res.better.zip', 'Destination (return)'),
        'is_return': fields.boolean(
            'Return Trip', help='Generate a return trip'),
        'departure': fields.datetime(
            'Desired Departure', help='Desired date and time of departure.'),
        'arrival': fields.datetime(
            'Desired Arrival', help='Desired date and time of Arrival.'),
        'return_departure': fields.datetime('Desired Departure (return)'),
        'return_arrival': fields.datetime('Desired Arrival (return)'),
        'class_id': fields.many2one(
            'travel.journey.class', 'Class', required=True,
            help='Desired class of voyage.'),
        'baggage_qty': fields.integer(
            'Baggage Quantity', help='Number of articles in baggage.'),
        'baggage_weight': fields.float(
            'Baggage Weight', help='Weight of baggage.'),
        'baggage_weight_uom': fields.many2one(
            'product.uom', 'Baggage Weight Unit of Measure',
            help='Unit of Measure for Baggage Weight'),
        'comment': fields.text('Comments'),
        'passenger_id': fields.many2one(
            'travel.passenger', 'Passenger', required=True,
            help='Passenger on this journey.'),
        'travel': fields.related(
            'passenger_id', 'travel_name', type='char', string='Travel'),
        'type': fields.selection(
            _get_type, 'Travel journey type', help='Travel journey type.'),
        'reservation': fields.char(
            'Reservation Number', size=256,
            help="Number of the ticket reservation."),
        'cancellation': fields.text(
            'Cancellation', help='Notes on cancellation.'),
        'gantt_date_start': fields.function(
            _gantt_date, fnct_inv=_inv_gantt_date, type="datetime"),
        'gantt_date_stop': fields.function(
            _gantt_date, fnct_inv=_inv_gantt_date, type="datetime"),
    }

    _defaults = {
        'class_id': _default_class
    }

    _constraints = [
        (check_date_exists,
         _('A desired date of arrival or departure must be set on journey.'),
         ['departure', 'arrival']),
        (check_date_exists_return,
         _('A desired date of arrival or departure must be set on journey for '
         'return.'),
         ['return_departure', 'return_arrival']),
        (check_date,
         _('Arrival date cannot be after departure date on journey.'),
         ['departure', 'arrival']),
        (check_date_return,
         _('Arrival date cannot be after departure date on journey for return.'),
         ['return_departure', 'return_arrival']),
        (check_uom,
         _('Unit of Measure not specified for Baggage Weight.'),
         ['budget', 'budget_currency', ])
    ]
