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

from openerp import fields, models, api, exceptions, _


class Travel(models.Model):
    """Travel"""

    _description = _(__doc__)
    _name = 'travel.travel'
    _inherit = ['mail.thread']

    name = fields.Char('Name of travel', required=True)
    city_ids = fields.Many2many(
        'res.better.zip',
        string='Locations',
        help='Destination cities of travel.',
    )
    date_start = fields.Date('Start Date', required=True)
    date_stop = fields.Date('End Date', required=True)
    passenger_ids = fields.One2many(
        'travel.passenger',
        'travel_id',
        'Passengers',
        help='List of passengers.',
    )
    manager_only = fields.Boolean(
        'Manager',
        function="is_manager_only",
        help='Can only be edited by a manager',
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('open', 'Saved'),
            ('booking', 'In Reservation'),
            ('reserved', 'Reserved'),
            ('confirmed', 'Confirmed'),
            ('done', 'Closed'),
        ],
        'Status',
        readonly=True,
        default='draft',
    )

    @api.multi
    def is_manager_only(self):
        limit = self.env['travel.config.settings'].get_basic_passenger_limit()
        return {t.id: len(t.passenger_ids) > limit for t in self}

    @api.constrains('date_start', 'date_stop')
    def check_date(self):
        if self.date_start > self.date_stop:
            raise exceptions.Warning(
                _('Start date cannot be after departure date.')
            )

    @api.model
    def create(self, vals):
        """
        Warn if user tried to create travel with too many passengers for
        according to his security role.
        """
        is_manager = self.env['res.users'].has_group(
            'travel.group_travel_manager'
        )
        limit = self.env['travel.config.settings'].get_basic_passenger_limit()
        if not is_manager and len(vals.get('passenger_ids', [])) > limit:
            raise exceptions.Warning(
                _('Only members of the Travel Managers group have the right '
                  'to create a Travel with more than %d passengers.') % limit)
        return super(Travel, self).create(vals)

    @api.multi
    def write(self, vals):
        """
        Warn if user does not have rights to modify travel with current number
        of  passengers or to add more than the limit.
        """
        is_manager = self.env['res.users'].has_group(
            'travel.group_travel_manager'
        )
        limit = self.env['travel.config.settings'].get_basic_passenger_limit()
        if not is_manager and len(vals.get('passenger_ids', [])) > limit:
            raise exceptions.Warning(
                _('Only members of the Travel Managers group have the rights '
                  'to add more than %d passengers to a travel.') % limit)
        for travel in self:
            if not is_manager and len(travel.passenger_ids) > limit:
                raise exceptions.Warning(
                    _('Only members of the Travel Managers group have the '
                      'rights to modify a Travel with more than %d passengers '
                      '(%s).') % (limit, travel.name))
        return super(Travel, self).write(vals)

    @api.multi
    def unlink(self):
        """Prevent deletion if travel isn't in draft

        Warn if ids being deleted contain a travel which has too many
        passengers for the current user to delete.
        """
        is_manager = self.env['res.users'].has_group(
            'travel.group_travel_manager'
        )
        limit = self.env['travel.config.settings'].get_basic_passenger_limit()
        for travel in self:
            if not is_manager and len(travel.passenger_ids) > limit:
                raise exceptions.Warning(
                    _('Only members of the Travel Managers group have the '
                      'rights to delete a Travel with more than %d passengers '
                      '(%s).') % (limit, travel.name))
            if travel.state != 'draft':
                raise exceptions.Warning(
                    _('Only draft travels can be unlinked'))

        return super(Travel, self).unlink()

    @api.multi
    def travel_open(self):
        """Put the state of the travel into open"""
        return self.write({'state': 'open'})

    @api.multi
    def travel_book(self):
        """Put the state of the travel into booking"""
        return self.write({'state': 'booking'})

    @api.multi
    def travel_reserve(self):
        """Put the state of the travel into reserved"""
        return self.write({'state': 'reserved'})

    @api.multi
    def travel_confirm(self):
        """Put the state of the travel into confirmed"""
        return self.write({'state': 'confirmed'})

    @api.multi
    def travel_close(self):
        """Put the state of the travel into done"""
        return self.write({'state': 'done'})
