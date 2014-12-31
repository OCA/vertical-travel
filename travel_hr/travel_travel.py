# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
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


# Based on _department_rule() from program_team
def _department_rule(self, cr, uid, ids, name, args, context=None):
    if isinstance(ids, (int, long)):
        ids = [ids]
    return {i: True for i in ids}


# Based on _department_rule_search() from program_team
def _department_rule_search(
        self, cr, uid, obj=None, name=None, args=None, context=None):
    user_pool = self.pool['res.users']

    if isinstance(args, list):
        # uid lies, so get current user from arguments
        user = args[0][2]
    else:
        user = args
    if isinstance(user, int):
        all_departments = user_pool.has_group(
            cr, user, 'travel_hr.group_travel_all_departments')
        user = user_pool.browse(cr, uid, user, context=context)
    else:
        all_departments = user_pool.has_group(
            cr, user.id, 'travel_hr.group_travel_all_departments')

    ids = [
        employee.department_id.id
        for employee in user.employee_ids
        if employee.department_id
    ]
    ids.append(False)
    if self._name != 'hr.department':
        if all_departments:
            query = []
        else:
            query = [('department_id', 'in', ids)]

        ids = self.search(
            cr, uid, query, context=context
        )
    return [('id', 'in', ids)]


class travel_travel(orm.Model):
    _inherit = 'travel.travel'

    def _get_department_id(self, cr, uid, context=None):
        context = context or {}

        employee_pool = self.pool['hr.employee']
        department_pool = self.pool['hr.department']
        query = [('user_id', '=', uid)]
        employee_id = employee_pool.search(
            cr, uid, query, limit=1, context=context)
        if employee_id:
            query = [('member_ids', 'in', employee_id)]
            department_id = department_pool.search(
                cr, uid, query, limit=1, context=context)
            return department_id and department_id[0] or False
        else:
            return False

    _columns = {
        'department_id': fields.many2one(
            'hr.department',
            'Department'
        ),
        'department_rule': fields.function(
            _department_rule,
            fnct_search=_department_rule_search,
            type='boolean',
            method=True,
            string="Department Rule",
        ),

    }

    _defaults = {
        'department_id': _get_department_id
    }
