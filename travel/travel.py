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


class travel_travel(orm.Model):
    _description = _('Travel')
    _name = 'travel.travel'
    _inherit = ['mail.thread']
    _columns = {
        'name': fields.char('Name', size=256, required=True, select=True,
                            help='Name of travel.'),
        'city_ids': fields.many2many('res.better.zip', string='Locations',
                                     help='Destination cities of travel.'),
        'date_start': fields.date('Start Date', required=True),
        'date_stop': fields.date('End Date', required=True),
        'passenger_ids': fields.one2many('travel.passenger', 'travel_id', 'Passengers',
                                         help='List of passengers.'),
        'state': fields.selection([('draft', 'Draft'),
                                   ('open', 'Saved'),
                                   ('booking', 'In Reservation'),
                                   ('reserved', 'Reserved'),
                                   ('confirmed', 'Confirmed'),
                                   ('done', 'Closed'),
                                   ], 'Status', readonly=True),
    }
    _defaults = {
        'state': 'draft',
    }

    def travel_open(self, cr, uid, ids, context=None):
        """Put the state of the travel into open"""
        for travel in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, [travel.id], {'state': 'open'})
        return True

    def travel_book(self, cr, uid, ids, context=None):
        """Put the state of the travel into booking"""
        for travel in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, [travel.id], {'state': 'booking'})
        return True

    def travel_reserve(self, cr, uid, ids, context=None):
        """Put the state of the travel into reserved"""
        for travel in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, [travel.id], {'state': 'reserved'})
        return True

    def travel_confirm(self, cr, uid, ids, context=None):
        """Put the state of the travel into confirmed"""
        for travel in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, [travel.id], {'state': 'confirmed'})
        return True

    def travel_close(self, cr, uid, ids, context=None):
        """Put the state of the travel into done"""
        for travel in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, [travel.id], {'state': 'done'})
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
