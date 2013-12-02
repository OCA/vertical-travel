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


class travel_journey_rail(orm.Model):
    _inherit = 'travel.journey'
    _columns = {
        'railway_station': fields.many2one('res.partner', 'Railway Station',
                                           domain="[('railway_station','=',True)]",
                                           help="Railway Station."),
        'railway_station_from': fields.many2one('res.partner', 'Origin',
                                                domain="[('railway_station','=',True)]",
                                                help="Departure Railway Station."),
        'railway_station_to': fields.many2one('res.partner', 'Destination',
                                              domain="[('railway_station','=',True)]",
                                              help="Destination Railway Station."),
        'railway_station_departure': fields.datetime('Departure',
                                                     help='Date and time of the departure of the train.'),
        'railway_station_arrival': fields.datetime('Arrival',
                                                   help='Date and time of the arrival of the train.'),
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
