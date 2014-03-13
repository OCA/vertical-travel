# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2010 - 2014 Savoir-faire Linux
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
from openerp.osv.osv import except_osv
from openerp.tools.translate import _


class travel_accommodation_import(orm.TransientModel):
    """Import data from other passengers"""
    _name = "travel.accommodation.import"
    _description = "Accommodation information import"
    _columns = {
        'travel_id': fields.many2one('travel.travel'),
        'cur_passenger_id': fields.many2one('travel.passenger'),
        'passenger_id': fields.many2one(
            'travel.passenger', string='Import Accommodation information from',
            help='Other passengers on the same journey.'),
    }

    def data_import(self, cr, uid, ids, context=None):
        """
        Import accommodation information from other passenger
        """
        tai_pool = self.pool.get('travel.accommodation.import')
        ta_pool = self.pool.get('travel.accommodation')
        passenger_id = False
        for tai_obj in tai_pool.browse(cr, uid, ids, context=context):
            cur_passenger_obj = tai_obj.cur_passenger_id
            other_passenger_obj = tai_obj.passenger_id
            if not other_passenger_obj:
                raise except_osv(_('Error'), _('No source passenger selected.'))
            passenger_id = cur_passenger_obj.id
            for acc_obj in other_passenger_obj.accommodation_ids:
                new_acc_id = ta_pool.copy(cr, uid, acc_obj.id, context=context)
                ta_pool.write(cr, uid, new_acc_id,
                              {'passenger_id': passenger_id}, context=context)
        return {
            'name': 'Passengers',
            'res_model': 'travel.passenger',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': passenger_id,
            'context': context,
        }

    def cancel(self, cr, uid, ids, context=None):
        tai_pool = self.pool.get('travel.accommodation.import')
        passenger_id = False
        for obj in tai_pool.browse(cr, uid, ids, context=context):
            passenger_id = obj.cur_passenger_id.id
        return {
            'name': 'Passengers',
            'res_model': 'travel.passenger',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': passenger_id,
            'context': context,
        }
