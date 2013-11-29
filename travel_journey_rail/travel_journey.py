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
        'railwaystation': fields.many2one('res.partner', 'Railway station',
                                          domain="[('railwaystation','=',True)]",
                                          help="Airline company."),
        'railwaystation_from': fields.many2one('res.partner', 'Origin',
                                               domain="[('railwaystation','=',True)]",
                                               help="Departure Railway station."),
        'railwaystation_to': fields.many2one('res.partner', 'Destination',
                                             domain="[('railwaystation','=',True)]",
                                             help="Destination Railway station."),
        'railwaystation_departure': fields.datetime('Departure',
                                                    help='Date and time of the departure of the rail.'),
        'railwaystation_arrival': fields.datetime('Arrival',
                                                  help='Date and time of the arrival of the rail.'),
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
