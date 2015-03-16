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
from openerp.tools.translate import _


class travel_passenger(orm.Model):

    """Passenger on travel"""
    _description = _(__doc__)
    _name = 'travel.passenger'
    _inherit = ['mail.thread']
    _rec_name = 'partner_id'
    _columns = {
        'partner_id': fields.many2one(
            'res.partner',
            'Passenger',
            required=True,
            ondelete='cascade',
            help="Name of Passenger.",
        ),
        'travel_id': fields.many2one(
            'travel.travel', 'Travel',
            help='Travel for which the passenger is participating.'),
        'travel_name': fields.related(
            'travel_id', 'name', type='char', string='Travel'),
        'travel_state': fields.related(
            'travel_id', 'state', type='selection', string='State'),
    }

    def name_get(self, cr, uid, ids, context=None):
        if type(ids) is not list:
            ids = [ids]
        return [(i.id, i.partner_id.name_get()[0][1])
                for i in self.browse(cr, uid, ids, context=context)]

    def action_passenger_form_view(self, cr, uid, ids, context=None):
        """Call action, if there is a travel, put it in the name."""
        if not ids:
            return {}
        if type(ids) is not list:
            ids = [ids]
        passenger = self.browse(cr, uid, ids, context=context)[0]
        travel = passenger.travel_id
        travel_name = ('%s / %s ' % (travel.name, passenger.name_get()[0][1]))
        name = travel_name or _('Passenger')
        context['default_date_start'] = travel.date_start
        context['default_date_stop'] = travel.date_stop
        return {
            'name': name,
            'res_model': 'travel.passenger',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': ids[0],
            'context': context,
        }

    def on_change_partner_id(self, cr, uid, ids, partner_id, context=None):
        """Placeholder function to be inherited"""
        res = {}
        return res
