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
from openerp import fields, models, api, exceptions, _
from openerp.tools.misc import (
    DEFAULT_SERVER_DATE_FORMAT,
    DEFAULT_SERVER_DATETIME_FORMAT,
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
        return not departure or not arrival or departure >= arrival

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
    def _estimate_date_start(self):
        return self._estimate_date('date_start')

    @api.one
    def _estimate_date_stop(self):
        return self._estimate_date('date_stop')

    @api.one
    def _estimate_date(self, field_name):
        return self._estimate_datetime(field_name)

    @api.one
    def _estimate_time(self, field_name):
        return self._estimate_datetime(field_name)

    @api.one
    def _inv_estimate_date_start(self):
        return self._inv_estimate_date('date_start')

    @api.one
    def _inv_estimate_date_stop(self):
        return self._inv_estimate_date('date_stop')

    @api.one
    def _inv_estimate_date(self, field_name):
        """If there is no start date in journey, set it in travel"""
        if field_name == 'date_start':
            if self.departure:
                self.write({'departure': self.date_start})
            elif self.passenger_id.travel_id.date_start:
                self.passenger_id.travel_id.write({'date_start':
                                                   self.date_start})
        elif field_name == 'date_stop':
            if self.arrival:
                self.write({'arrival': self.date_stop})
            elif self.passenger_id.travel_id.date_stop:
                self.passenger_id.travel_id.write({'date_stop':
                                                   self.date_stop})

    @api.one
    def _default_class(self):
        return self.env['ir.model.data'].get_object_reference(
            'travel_journey', 'travel_journey_class_directive')[1]

    @api.one
    def _get_journey_type(self):
        res = self.env['travel.journey.type'].search()
        return [(r.code, r.name) for r in res]

    @api.one
    def create(self, vals):
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
        res = super(TravelJourney, self).create(vals)
        if return_vals:
            super(TravelJourney, self).create(return_vals)
        return res

    @api.onchange('origin')
    def onchange_origin(self):
        if self.origin:
            self.return_destination = self.origin

    @api.onchange('destination')
    def onchange_destination(self):
        if self.destination:
            self.return_origin = self.destination

    @api.one
    @api.constrains('departure', 'arrival')
    def check_date_exists(self):
        if self.departure is None and self.arrival is None:
            raise exceptions.ValidationError(
                _('A desired date of arrival or departure '
                  'must be set on journey.'))

    @api.one
    @api.constrains('is_return', 'return_departure', 'return_arrival')
    def check_date_exists_return(self):
        if self.is_return and (self.return_departure is None or
                               self.return_arrival is None):
            raise exceptions.ValidationError(
                _('A desired date of arrival or departure must be '
                  'set on journey for .'))

    @api.one
    @api.constrains('departure', 'arrival')
    def check_date(self):
        if self._check_dep_arr_dates(self.departure, self.arrival):
            raise exceptions.ValidationError(
                _('Departure date cannot be after arrival date on journey.'))

    @api.one
    @api.constrains('return_departure', 'return_arrival')
    def check_date_return(self):
        if self.is_return:
            if self._check_dep_arr_dates(self.return_departure,
                                         self.return_arrival):
                raise exceptions.ValidationError(
                    _('Departure date cannot be after arrival '
                      'date on journey for return.'))

    @api.one
    @api.constrains('baggage_weight', 'baggage_weight_uom')
    def check_uom(self):
        # uom can be null if there is 0 ludgage
        if (bool(self.baggage_weight) ^
                bool(self.baggage_weight_uom)):
            raise exceptions.ValidationError(
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
        'res.better.zip',
        string='Origin',
        required='True',
        help='Source city of travel.'
    )
    destination = fields.Many2one(
        'res.better.zip',
        string='Destination',
        required='True',
        help='Destination city of travel.')
    return_origin = fields.Many2one(
        'res.better.zip',
        string='Origin (return)',
    )
    return_destination = fields.Many2one(
        'res.better.zip',
        string='Destination (return)',
    )
    is_return = fields.Boolean(
        string='Return Trip',
        help='Generate a return trip'
    )
    departure = fields.Datetime(
        string='Desired Departure',
        help='Desired date and time of departure.'
    )
    arrival = fields.Datetime(
        string='Desired Arrival',
        help='Desired date and time of Arrival.'
    )
    return_departure = fields.Datetime('Desired Departure (return)')
    return_arrival = fields.Datetime('Desired Arrival (return)')
    class_id = fields.Many2one(
        'travel.journey.class',
        string='Class',
        default='_default_class',
        required=True,
        help='Desired class of voyage.'
    )
    baggage_qty = fields.Integer(
        string='Baggage Quantity',
        help='Number of articles in baggage.'
    )
    baggage_weight = fields.Float(
        string='Baggage Weight',
        help='Weight of baggage.'
    )
    baggage_weight_uom = fields.Many2one(
        'product.uom',
        string='Baggage Weight Unit of Measure',
        help='Unit of Measure for Baggage Weight'
    )
    comment = fields.Text('Comments')
    passenger_id = fields.Many2one(
        'travel.passenger',
        string='Passenger',
        required=True,
        help='Passenger on this journey.'
    )
    travel = fields.Char(
        string='Travel',
        related='passenger_id.travel_name',
        store=True
    )
    state = fields.Selection(
        string='State',
        related='passenger_id.travel_state',
        store=True
    )
    journey_type = fields.Selection(
        string='Travel journey type',
        selection='_get_journey_type',
        help='Travel journey type.'
    )
    reservation = fields.Char(
        string='Reservation Number',
        help="Number of the ticket reservation."
    )
    cancellation = fields.Text('Cancellation', help='Notes on cancellation.')
    date_start = fields.Date(
        string="Start Date",
        compute='_estimate_date_start',
        fnct_inv='_inv_estimate_date_start',
        type="date",
        help="Best estimate of start date calculated from filled fields."
    )
    date_stop = fields.Date(
        string="Stop Date",
        compute='_estimate_date_stop',
        fnct_inv='_inv_estimate_date_stop',
        type="date",
        help="Best estimate of end date calculated from filled fields.",
    )
