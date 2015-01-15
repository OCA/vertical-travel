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
from .res_config import get_basic_passenger_limit, get_alert_address


class travel_travel(orm.Model):

    """Travel"""
    _description = _(__doc__)
    _name = 'travel.travel'
    _inherit = ['mail.thread']

    def is_manager_only(self, cr, user, ids, name, args, context=None):
        limit = get_basic_passenger_limit(self.pool.get("ir.config_parameter"),
                                          cr, user, context=context)
        return {t.id: len(t.passenger_ids) > limit
                for t in self.browse(cr, user, ids, context=context)}

    def _get_responsible_emails(
            self, cr, uid, ids, name=None, args=None, context=None):
        context = context or {}
        res = {}

        for travel in self.browse(cr, uid, ids, context=context):
            if travel.state == 'open':
                ctx = dict(context, alert_type='sent')
                res[travel.id] = get_alert_address(
                    self.pool.get("ir.config_parameter"), cr, uid, context=ctx)
            elif travel.state == 'reserved':
                if travel.user_id.email:
                    res[travel.id] = travel.user_id.email
                else:
                    raise orm.except_orm(
                        _('Warning'),
                        _('Responsible user has no e-mail set.')
                    )

        return res

    _columns = {
        'name': fields.char('Name of travel', required=True,
                            help='Name of travel.'),
        'city_ids': fields.many2many('res.better.zip', string='Locations',
                                     help='Destination cities of travel.'),
        'date_start': fields.date('Start Date', required=True),
        'date_stop': fields.date('End Date', required=True),
        'passenger_ids': fields.one2many('travel.passenger', 'travel_id',
                                         'Passengers',
                                         help='List of passengers.'),
        'manager_only': fields.function(is_manager_only,
                                        store=True,
                                        type='boolean',
                                        string='Manager'),
        'state': fields.selection([('draft', 'Draft'),
                                   ('open', 'Saved'),
                                   ('booking', 'In Reservation'),
                                   ('reserved', 'Reserved'),
                                   ('confirmed', 'Confirmed'),
                                   ('done', 'Closed'),
                                   ], 'Status', readonly=True),
        'responsible_emails': fields.function(_get_responsible_emails,
                                              type='char',
                                              string='Responsible e-mails'),
        'user_id': fields.many2one('res.users', 'Responsible'),
    }
    _defaults = {
        'state': 'draft',
        'user_id': lambda self, cr, uid, ctx: uid
    }

    def check_date(self, cr, uid, ids, context=None):
        if not ids:  # pragma: no cover
            return False
        travel = self.browse(cr, uid, ids[0], context=context)
        return travel.date_start <= travel.date_stop

    _constraints = [
        (check_date,
         _('Start date cannot be after departure date.'),
         ['date_start', 'date_stop']),
    ]

    def create(self, cr, user, vals, context=None):
        """
        Warn if user tried to create travel with too many passengers for
        according to his security role.
        """
        users_pool = self.pool.get('res.users')
        limit = get_basic_passenger_limit(self.pool.get("ir.config_parameter"),
                                          cr, user, context=context)
        if (len(vals.get('passenger_ids', [])) > limit and not
                users_pool.has_group(cr, user, 'travel.group_travel_manager')):
            raise orm.except_orm(
                _('Warning!'),
                _('Only members of the Travel Managers group have the right '
                  'to create a Travel with more than %d passengers.') % limit)
        return super(travel_travel, self).create(
            cr, user, vals, context=context)

    def write(self, cr, user, ids, vals, context=None):
        """
        Warn if user does not have rights to modify travel with current number
        of  passengers or to add more than the limit.
        """
        if type(ids) is not list:
            ids = [ids]
        users_pool = self.pool.get('res.users')
        limit = get_basic_passenger_limit(self.pool.get("ir.config_parameter"),
                                          cr, user, context=context)
        if (len(vals.get('passenger_ids', [])) > limit and not
                users_pool.has_group(cr, user, 'travel.group_travel_manager')):
            raise orm.except_orm(
                _('Warning!'),
                _('Only members of the Travel Managers group have the rights '
                  'to add more than %d passengers to a travel.') % limit)
        for travel in self.browse(cr, user, ids, context=context):
            if (len(travel.passenger_ids) > limit and not
                    users_pool.has_group(cr, user,
                                         'travel.group_travel_manager')):
                raise orm.except_orm(
                    _('Warning!'),
                    _('Only members of the Travel Managers group have the '
                      'rights to modify a Travel with more than %d passengers '
                      '(%s).') % (limit, travel.name))
        return super(travel_travel, self).write(cr, user, ids, vals,
                                                context=context)

    def unlink(self, cr, user, ids, context=None):
        """
        Warn if ids being deleted contain a travel which has too many
        passengers for the current user to delete.
        """
        if type(ids) is not list:
            ids = [ids]
        users_pool = self.pool.get('res.users')
        limit = get_basic_passenger_limit(self.pool.get("ir.config_parameter"),
                                          cr, user, context=context)
        for travel in self.browse(cr, user, ids, context=context):
            if (len(travel.passenger_ids) > limit and not
                    users_pool.has_group(cr, user,
                                         'travel.group_travel_manager')):
                raise orm.except_orm(
                    _('Warning!'),
                    _('Only members of the Travel Managers group have the '
                      'rights to delete a Travel with more than %d passengers '
                      '(%s).') % (limit, travel.name))
            if travel.state != 'draft':
                raise orm.except_orm(
                    _('Warning!'),
                    _('Only draft travels can be unlinked'))

        return super(travel_travel, self).unlink(
            cr, user, ids, context=context)

    def travel_open(self, cr, uid, ids, context=None):
        """Put the state of the travel into open"""
        if type(ids) is not list:
            ids = [ids]
        for travel in self.browse(cr, uid, ids, context=context):
            self.write(
                cr, uid, [travel.id], {'state': 'open', 'user_id': uid},
                context=context)
        return True

    def travel_book(self, cr, uid, ids, context=None):
        """Put the state of the travel into booking"""
        if type(ids) is not list:
            ids = [ids]
        for travel in self.browse(cr, uid, ids, context=context):
            self.write(
                cr, uid, [travel.id], {'state': 'booking'}, context=context)
        return True

    def travel_reserve(self, cr, uid, ids, context=None):
        """Put the state of the travel into reserved"""
        if type(ids) is not list:
            ids = [ids]
        for travel in self.browse(cr, uid, ids, context=context):
            self.write(
                cr, uid, [travel.id], {'state': 'reserved'}, context=context)
        return True

    def travel_confirm(self, cr, uid, ids, context=None):
        """Put the state of the travel into confirmed"""
        if type(ids) is not list:
            ids = [ids]
        for travel in self.browse(cr, uid, ids, context=context):
            self.write(
                cr, uid, [travel.id], {'state': 'confirmed'}, context=context)
        return True

    def travel_close(self, cr, uid, ids, context=None):
        """Put the state of the travel into done"""
        if type(ids) is not list:
            ids = [ids]
        for travel in self.browse(cr, uid, ids, context=context):
            self.write(
                cr, uid, [travel.id], {'state': 'done'}, context=context)
        return True
