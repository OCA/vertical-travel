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


class travel_journey(orm.Model):
    _description = 'Journey of travel'
    _name = 'travel.journey'

    def on_change_location(self, cr, uid, ids, location, context=None):
        return {'value': {'return_origin': location}}

    _columns = {
        'origin': fields.many2one('res.country.city', 'Origin', required='True',
                                  help='Source city of travel.'),
        'destination': fields.many2one('res.country.city', 'Destination', required='True',
                                       help='Destination city of travel.'),
        'return_origin': fields.many2one('res.country.city', 'Origin (return)', readonly=True),
        'return': fields.boolean('Return Trip', help='Generate a return trip'),
        # TODO: One and only one of the following two has to be filled
        'departure': fields.datetime('Desired Departure',
                                     help='Desired date and time of departure.'),
        'arrival': fields.datetime('Desired Arrival',
                                   help='Desired date and time of Arrival.'),
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
    }

    def _default_class(self, cr, uid, context=None):
        ir_model_data = self.pool.get('ir.model.data')
        return ir_model_data.get_object_reference(cr, uid, 'travel_journey',
                                                  'travel_journey_class_directive',)[1]

    _defaults = {
        'class_id': _default_class
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
