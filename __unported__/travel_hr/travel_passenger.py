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
from .travel_travel import _department_rule, _department_rule_search


class travel_passenger(orm.Model):
    _inherit = 'travel.passenger'
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

    def get_employees_from_partner_ids(
            self, cr, uid, partner_ids, context=None):
        """
        Given a list of partner_id find the hr.employee who have it in their
        related user's partner_id.
        """
        res = []
        if type(partner_ids) in (int, long):
            partner_ids = [partner_ids]
        elif partner_ids is False:
            return res
        hr_employee_pool = self.pool.get('hr.employee')
        for partner_id in partner_ids:
            employee_id = hr_employee_pool.search(
                cr, uid, [('user_id.partner_id', '=', partner_id)], limit=1,
                context=context)
            if len(employee_id) == 1:
                employee = hr_employee_pool.browse(
                    cr, uid, employee_id[0], context=context)
                res.append(employee)
        return res

    def get_departments_from_partner_ids(
            self, cr, uid, partner_ids, context=None):
        if type(partner_ids) in (int, long):
            partner_ids = [partner_ids]
        employees = self.get_employees_from_partner_ids(
            cr, uid, partner_ids, context=context)
        res = [o.department_id.id for o in employees
               if o and o.department_id]
        return res

    def on_change_partner_id(self, cr, uid, ids, partner_id, context=None):
        """Try and get an hr.department from the res.partner"""
        res = super(travel_passenger, self).on_change_partner_id(
            cr, uid, ids, partner_id, context=context)
        # Find department related to res.partner through employee's user
        department_ids = self.get_departments_from_partner_ids(
            cr, uid, partner_id, context=context)
        department_id = department_ids[0] if department_ids else False
        # Fill in and return found values
        value = res.get('value', {})
        value['department_id'] = department_id
        res['value'] = value
        return res

    def create(self, cr, uid, vals, context=None):
        """
        Try and get an hr.department added manually as the field is readonly
        """
        partner_id = vals.get('partner_id')
        if partner_id:
            department_ids = self.get_departments_from_partner_ids(
                cr, uid, partner_id, context=context)
            if department_ids:
                vals['department_id'] = department_ids[0]
        return super(travel_passenger, self).create(
            cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        """
        Try and get an hr.department added manually as the field is readonly
        """
        partner_id = vals.get('partner_id')
        if partner_id:
            department_ids = self.get_departments_from_partner_ids(
                cr, uid, partner_id, context=context)
            if department_ids:
                vals['department_id'] = department_ids[0]
        return super(travel_passenger, self).write(
            cr, uid, ids, vals, context=context)
