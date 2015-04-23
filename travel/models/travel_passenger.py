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

from openerp import fields, models, api, _


class TravelPassenger(models.Model):
    """Passenger on travel"""

    _name = 'travel.passenger'
    _description = _(__doc__)
    _inherit = ['mail.thread']
    _rec_name = 'partner_id'
    partner_id = fields.Many2one(
        'res.partner',
        'Passenger',
        required=True,
        ondelete='cascade',
        help="Name of Passenger.",
    )
    travel_id = fields.Many2one(
        'travel.travel',
        'Travel',
        help='Travel for which the passenger is participating.'
    )
    travel_name = fields.Char(
        string='Travel',
        related='travel_id.name',
    )
    travel_state = fields.Selection(
        string='State',
        related='travel_id.state',
    )

    @api.multi
    def name_get(self):
        """Get name of partner"""
        return [(i.id, i.partner_id.name_get()[0][1]) for i in self]

    @api.multi
    def action_passenger_form_view(self):
        """Call action, if there is a travel, put it in the name.

        Insert default dates in context
        """
        self.ensure_one()
        travel = self.travel_id
        if not travel:
            return {}  # pragma: no cover
        travel_name = ('%s / %s ' % (travel.name, self.name_get()[0][1]))
        name = travel_name or _('Passenger')
        context = dict(
            self._context,
            default_date_start=travel.date_start,
            default_date_stop=travel.date_stop
        )
        return {
            'name': name,
            'res_model': 'travel.passenger',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
            'context': context,
        }

    @api.onchange('partner_id')
    def on_change_partner_id(self):
        """Placeholder function to be inherited"""
        res = {}
        return res
