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


class travel_accommodation_import(orm.TransientModel):
    """Import data from other passengers"""
    _name = "travel.accommodation.import"
    _description = "Accommodation information import"
    _columns = {
        'travel_id': fields.many2one('travel.travel'),
        'cur_passenger_id': fields.many2one('travel.passenger'),
        'passenger_id': fields.many2one('travel.passenger',
                                        string='Import Accommodation information from',
                                        help='Other passengers on the same journey.'),
    }

    def data_import(self, cr, uid, ids, context=None):
        """
        Import accommodation information from other passenger
        """
        tai_pool = self.pool.get('travel.accommodation.import')
        for tai_obj in tai_pool.browse(cr, uid, ids, context=context):
            cur_passenger_obj = tai_obj.cur_passenger_id
            other_passenger_obj = tai_obj.passenger_id
            vals = {
                'accommodation_ids': [(6, 0, [i.id for i in other_passenger_obj.accommodation_ids])],
            }
            cur_passenger_obj.write(vals)
        return {'type': 'ir.actions.act_window_close'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
