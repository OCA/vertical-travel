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

from datetime import datetime
from openerp import fields, models, api, _
from openerp.tools.misc import (
    DEFAULT_SERVER_DATE_FORMAT,
    DEFAULT_SERVER_DATETIME_FORMAT,
    DEFAULT_SERVER_TIME_FORMAT,
)

import logging
_logger = logging.getLogger(__name__)


class TravelJourney(models.Model):

    """Journey of travel"""
    _name = 'travel.journey'
    _description = _(__doc__)
    _journey_type_classes = {}
    _rec_name = 'destination'

    @staticmethod
    def _check_dep_arr_dates(departure, arrival):
        return not departure or not arrival or departure <= arrival
    
    @api.one
    def _estimate_datetime(self, field_name):
        """If there is no start date from journey, get it from travel"""
        res = {}
        date = False

        if self.journey_type:
            try:
                journey_class = self._journey_type_classes[self.journey_type]
                date = journey_class._estimate_typed_date(
                    self, self, field_name)
            except KeyError:
                _logger.error(
                    _('Transportation type "%s" has not registered its '
                      'class in _journey_types, skipping its dates')
                    % self.journey_type)
            except AttributeError:
                _logger.error(
                    _('Transportation type "%s" has not registered a '
                      '_estimate_typed_date() function, skipping its '
                      'dates')
                    % self.journey_type)
        if field_name == 'date_start':
            date = (date or self.departure or
                    self.passenger_id.travel_id.date_start)
        elif field_name == 'date_stop':
            date = (date or self.arrival or
                    self.passenger_id.travel_id.date_stop)
        # Make sure every date is in datetime format and not simply date
        try:
            date = datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        except ValueError:
            date = datetime.strptime(date, DEFAULT_SERVER_DATETIME_FORMAT)
        res[self.id] = date
        
        return res

    @api.one
    def _estimate_date(self, field_name):
        datetimes = self._estimate_datetime(field_name)
        return {
            i: datetimes[i].strftime(DEFAULT_SERVER_DATE_FORMAT)
            for i in datetimes
        }

    @api.one
    def _estimate_time(self, field_name):
        datetimes = self._estimate_datetime(field_name)
        return {
            i: datetimes[i].strftime(DEFAULT_SERVER_TIME_FORMAT)
            for i in datetimes
        }

    def _inv_estimate_date(self, cr, uid, ids, field_name, val, arg,
                           context=None):
        """If there is no start date in journey, set it in travel"""
        if type(ids) in (int, long):
            ids = [ids]
        for journey in self.browse(cr, uid, ids, context=context):
            if journey.journey_type:
                try:
                    journey_class = self._journey_type_classes[journey.journey_type]
                    if (journey_class._inv_estimate_typed_date(
                            self, journey, field_name, val)):
                        continue
                except KeyError:
                    _logger.error(
                        _('Transportation type "%s" has not registered its '
                          'class in _journey_types, skipping its dates')
                        % journey.journey_type)
                except AttributeError:
                    _logger.error(
                        _('Transportation type "%s" has not registered a '
                          '_inv_estimate_typed_date() function, skipping its '
                          'dates') % journey.journey_type)
            if field_name == 'date_start':
                if journey.departure:
                    journey.write({'departure': val})
                elif journey.passenger_id.travel_id.date_start:
                    journey.passenger_id.travel_id.write({'date_start': val})
            elif field_name == 'date_stop':
                if journey.arrival:
                    journey.write({'arrival': val})
                elif journey.passenger_id.travel_id.date_stop:
                    journey.passenger_id.travel_id.write({'date_stop': val})

    @api.one
    def _default_class(self):
        return self.env['ir.model.data'].get_object_reference(
                'travel_journey', 'travel_journey_class_directive')[1]
    
    @api.one
    def _get_journey_type(self):
#         if type(ids) is dict and context is None:
#             context = ids
        res = self.env['travel.journey.type'].search(cr, uid, [])
        #res = acc_type_obj.read(cr, uid, ids, ['code', 'name'], context)
        return [(r.code, r.name) for r in res]
    
    @api.v7
    def create(self, cr, uid, vals, context=None):
        """If is_return is checked, create a return trip after."""
        def clear_return_vals(mVals):
            mVals = mVals.copy()
            if mVals.get('is_return'):
                mVals['is_return'] = False
                mVals['return_origin'] = False
                mVals['return_destination'] = False
                mVals['return_departure'] = False
                mVals['return_arrival'] = False
            return mVals
        return_vals = None
        if vals.get('is_return'):
            return_vals = clear_return_vals(vals.copy())
            return_vals['is_return'] = False
            return_vals['origin'] = vals.get('destination', False)
            return_vals['destination'] = vals.get('origin', False)
            return_vals['departure'] = vals.get('return_departure', False)
            return_vals['arrival'] = vals.get('return_arrival', False)
        vals = clear_return_vals(vals)
        res = super(travel_journey, self).create(
            cr, uid, vals, context=context
        )
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
        # Remove the return_arrival=False or return_arrival=False
        # because we get the popup message two times.
        # Anyway another control exists
        # if you want to validate the form with bad dates.
        return {
            'warning': {
                'title': _('Arrival after Departure'),
                'message': _('Departure (%s) cannot be before Arrival (%s).') %
                            (departure, arrival),
            },
        }
    
    @api.one
    @api.constrains('departure','arrival')
    def check_date_exists(self):
        if self.departure is None and self.arrival is None:
            raise ValidationError(
                _('A desired date of arrival or departure '
                'must be set on journey.'))
        

    @api.one
    @api.constrains('is_return','return_departure','return_arrival')
    def check_date_exists_return(self):
        if self.is_return and (self.return_departure is None or
                               self.return_arrival is None): 
           raise ValidationError(
              _('A desired date of arrival or departure must be '
                 'set on journey for .'))
    
    @api.one
    @api.constrains('departure','arrival')
    def check_date(self):
        if self._check_dep_arr_dates(self.departure, self.arrival):
            raise ValidationError(
               _('Departure date cannot be after arrival date on journey.'))

    @api.one
    @api.constrains('return_departure','return_arrival')
    def check_date_return(self):
        if self._check_dep_arr_dates(self.return_departure, 
                                     self.return_arrival):
            raise ValidationError(
               _('Departure date cannot be after arrival '
                 'date on journey for return.'))

    @api.one
    @api.constrains('baggage_weight','baggage_weight_uom')
    def check_uom(self):
        if not (bool(self.baggage_weight) ^
                    bool(self.baggage_weight_uom)):
           raise ValidationError(
              _('Unit of Measure not specified for Baggage Weight.'))
    
    @api.multi
    def name_get(self):
        return [
            (journey.id,
             "%s (%s -> %s)" % (journey.passenger_id.partner_id.name,
                                journey.origin.name_get()[0][1],
                                journey.destination.name_get()[0][1]))
            for journey in self
        ]

    @api.one
    def company_get(self):
        res = _("N/A")
        try:
            if self.journey_type:
                journey_class = self._journey_type_classes[self.journey_type]
                res = journey_class._company_typed_get(self, self)
        except KeyError:
            _logger.error(
                _('Transportation type "%s" has not registered its '
                  'class in _journey_types, skipping its company')
                % self.journey_type)
        except AttributeError:
            _logger.error(
                _('Transportation type "%s" has not registered a '
                  '_estimate_typed_date() function, skipping its company')
                % self.journey_type)
        finally:
            return res
    
    @api.one
    def origin_get(self):
        return self.origin

    @api.one
    def destination_get(self):
        return self.destination

    @api.one
    def departure_date_get(self):
        return self._estimate_date('date_start')
    
    @api.one
    def arrival_date_get(self):
        return self._estimate_date('date_stop')
    
    @api.one
    def departure_time_get(self):
        return self._estimate_time('date_start')

    @api.one
    def arrival_time_get(self):
        return self._estimate_time('date_stop')
    
    origin = fields.Many2one(
       'Origin', 
       'res.better.zip', 
       required='True',
       help='Source city of travel.'
    )
    destination = fields.Many2one(
       'Destination',
       'res.better.zip', 
       required='True',
       help='Destination city of travel.')
    return_origin = fields.Many2one(
       'Origin (return)',
       'res.better.zip'
    )
    return_destination = fields.Many2one(
       'Destination (return)',
       'res.better.zip'
    )
    is_return = fields.Boolean(
       'Return Trip', 
       help='Generate a return trip'
    )
    departure = fields.Datetime(
       'Desired Departure', 
       help='Desired date and time of departure.'
    )
    arrival = fields.Datetime(
       'Desired Arrival', 
       help='Desired date and time of Arrival.'
    )
    return_departure = fields.Datetime('Desired Departure (return)')
    return_arrival = fields.Datetime('Desired Arrival (return)')
    class_id = fields.Many2one(
       'Class',
       'travel.journey.class',
       default= _default_class,
       required=True,
       help='Desired class of voyage.'
    )
    baggage_qty = fields.Integer(
       'Baggage Quantity', 
       help='Number of articles in baggage.'
    )
    baggage_weight = fields.Float(
       'Baggage Weight', 
       help='Weight of baggage.'
    )
    baggage_weight_uom = fields.Many2one(
       'Baggage Weight Unit of Measure',
       'product.uom', 
       help='Unit of Measure for Baggage Weight'
    )
    comment = fields.Text('Comments')
    passenger_id = fields.Many2one(
       'Passenger', 
       'travel.passenger', 
       required=True,
       help='Passenger on this journey.'
    )
    travel = fields.Char(
       string='Travel',
       related = 'passenger_id.travel_name',
       store=True
    )
    state = fields.Selection(
       string='State', 
       related='passenger_id.travel_state', 
       store=True
    )
    journey_type = fields.Selection(
       'Travel journey type',
       _get_journey_type, 
       help='Travel journey type.'
    )
    reservation = fields.Char(
       'Reservation Number', 
       help="Number of the ticket reservation."
    )
    cancellation = fields.Text('Cancellation', help='Notes on cancellation.')
    date_start = fields.Function(
       string="Start Date",
       _estimate_date,
       fnct_inv=_inv_estimate_date,
       type="date",
       help="Best estimate of start date calculated from filled fields."
    )
    date_stop = fields.Function(
       string="Stop Date",
       _estimate_date,
       fnct_inv=_inv_estimate_date,
       type="date",
       help="Best estimate of end date calculated from filled fields.",
    )

