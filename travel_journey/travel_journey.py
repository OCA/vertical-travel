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


def _get_type(self, cr, uid, context=None):
    acc_type_obj = self.pool.get('travel.journey.type')
    ids = acc_type_obj.search(cr, uid, [])
    res = acc_type_obj.read(cr, uid, ids, ['code', 'name'], context)
    return [(r['code'], r['name']) for r in res]


class travel_journey(orm.Model):
    _description = _('Journey of travel')
    _name = 'travel.journey'
    _columns = {
        'origin': fields.many2one('res.country.city', 'Origin', required='True',
                                  help='Source city of travel.'),
        'destination': fields.many2one('res.country.city', 'Destination', required='True',
                                       help='Destination city of travel.'),
        'return_origin': fields.many2one('res.country.city', 'Origin (return)'),
        'return_destination': fields.many2one('res.country.city', 'Destination (return)'),
        'is_return': fields.boolean('Return Trip', help='Generate a return trip'),
        # TODO: One and only one of the following two has to be filled
        'departure': fields.datetime('Desired Departure',
                                     help='Desired date and time of departure.'),
        'arrival': fields.datetime('Desired Arrival',
                                   help='Desired date and time of Arrival.'),
        'return_departure': fields.datetime('Desired Departure (return)'),
        'return_arrival': fields.datetime('Desired Arrival (return)'),
        'visa': fields.boolean('Visa Required',
                               help='Is a visa required to visit destination city?'),
        # TODO: make following field only visible if previous field is true
        'visa_country': fields.many2one('res.country', 'Country Visa',
                                        help='Country for which a visa is needed'),
        'class_id': fields.many2one('travel.journey.class', 'Class', required=True,
                                    help='Desired class of voyage.'),
        'baggage_qty': fields.integer('Baggage Quantity', help='Number of articles in baggage.'),
        'baggage_weight': fields.float('Baggage Weight', help='Weight of baggage.'),
        # TODO: change the previous when the following changes
        'baggage_weight_uom': fields.many2one('product.uom', 'Baggage Weight Unit of Measure',
                                              help='Unit of Measure for Baggage Weight'),
        'comment': fields.text('Comments'),
        'passenger_id': fields.many2one('travel.passenger', 'Passenger', required=True,
                                        help='Passenger on this journey.'),
        'type': fields.selection(_get_type, 'Travel journey type',
                                 help='Travel journey type.'),
        'reservation': fields.char('Reservation Number', size=256,
                                   help="Number of the ticket reservation."),
        'cancellation': fields.text('Cancellation', help='Notes on cancellation.'),
    }

    def _default_class(self, cr, uid, context=None):
        ir_model_data = self.pool.get('ir.model.data')
        return ir_model_data.get_object_reference(cr, uid, 'travel_journey',
                                                  'travel_journey_class_directive',)[1]

    _defaults = {
        'class_id': _default_class
    }

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
            super(travel_journey, self).create(cr, uid, return_vals, context=context)
        return res

    def on_change_return(self, cr, uid, ids, key, location, context=None):
        return {'value': {key: location}}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
