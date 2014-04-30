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

from openerp.tests.common import TransactionCase
from openerp.osv.orm import except_orm
import time


class test_travel(TransactionCase):

    def setUp(self):
        super(test_travel, self).setUp()
        # Clean up registries
        self.registry('ir.model').clear_caches()
        self.registry('ir.model.data').clear_caches()
        # Get registries
        self.user_model = self.registry("res.users")
        self.travel_model = self.registry("travel.travel")
        # Get context
        self.context = self.user_model.context_get(self.cr, self.uid)
        # Create values for test, travel and partner also created
        self.year = str(time.localtime(time.time())[0])
        self.vals = {
            'name': 'This is a test travel name',
            'date_start': self.year + '-01-01',
            'date_stop': self.year + '-01-14',
        }

    def test_create_travel(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        self.assertTrue(self.travel_model.create(
            cr, uid, vals, context=context))

    def test_write_travel(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        travel_id = self.travel_model.create(cr, uid, vals, context=context)
        self.travel_model.write(cr, uid, travel_id, {
            'date_stop': self.year + '-01-21',
        }, context=context)

    def test_unlink_travel(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        travel_id = self.travel_model.create(cr, uid, vals, context=context)
        self.travel_model.unlink(cr, uid, travel_id, context=context)

    def test_change_state_travel(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        states = {
            'open': self.travel_model.travel_open,
            'booking': self.travel_model.travel_book,
            'reserved': self.travel_model.travel_reserve,
            'confirmed': self.travel_model.travel_confirm,
            'done': self.travel_model.travel_close,
        }
        travel_id = self.travel_model.create(cr, uid, vals, context=context)
        for state, func in states.iteritems():
            func(cr, uid, travel_id, context=context)
            travel_obj = self.travel_model.browse(
                cr, uid, travel_id, context=context)
            self.assertEqual(travel_obj.state, state)

    def test_create_travel_too_many_passengers(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        partner_model = self.registry("res.partner")
        group_id = self.registry("ir.model.data").get_object_reference(
            cr, uid, 'travel', 'group_basic_travel_user')[1]
        user_id = self.user_model.create(cr, uid, {
            'login': 'test',
            'name': 'test',
            'groups_id': [(4, group_id)],
        }, context=context)
        vals = vals.copy()
        vals["passenger_ids"] = []
        for i in xrange(12):
            partner_id = partner_model.create(
                cr, uid, {'name': 'test_partner_%d' % i}, context=context)
            vals["passenger_ids"].append(tuple([0, 0,  {
                "partner_id": partner_id,
            }]))
        self.assertRaises(
            except_orm,
            self.travel_model.create,
            cr, user_id, vals, context=context
        )

    def test_write_travel_too_many_passengers(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        travel_id = self.travel_model.create(cr, uid, vals, context=context)
        partner_model = self.registry("res.partner")
        group_id = self.registry("ir.model.data").get_object_reference(
            cr, uid, 'travel', 'group_basic_travel_user')[1]
        user_id = self.user_model.create(cr, uid, {
            'login': 'test',
            'name': 'test',
            'groups_id': [(4, group_id)],
        }, context=context)
        vals = {
            "passenger_ids": [],
        }
        for i in xrange(12):
            partner_id = partner_model.create(
                cr, uid, {'name': 'test_partner_%d' % i}, context=context)
            vals["passenger_ids"].append(tuple([0, 0, {
                "partner_id": partner_id,
            }]))
        self.assertRaises(
            except_orm,
            self.travel_model.write,
            cr, user_id, travel_id, vals, context=context
        )
        self.travel_model.write(cr, uid, travel_id, vals, context=context)
        self.assertRaises(
            except_orm,
            self.travel_model.write,
            cr, user_id, travel_id, vals={'name': 'changed'}, context=context
        )

    def test_unlink_travel_too_many_passengers(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        partner_model = self.registry("res.partner")
        group_id = self.registry("ir.model.data").get_object_reference(
            cr, uid, 'travel', 'group_basic_travel_user')[1]
        user_id = self.user_model.create(cr, uid, {
            'login': 'test',
            'name': 'test',
            'groups_id': [(4, group_id)],
        }, context=context)
        vals = vals.copy()
        vals["passenger_ids"] = []
        for i in xrange(12):
            partner_id = partner_model.create(
                cr, uid, {'name': 'test_partner_%d' % i}, context=context)
            vals["passenger_ids"].append(tuple([0, 0, {
                "partner_id": partner_id,
            }]))
        travel_id = self.travel_model.create(cr, uid, vals, context=context)
        self.assertRaises(
            except_orm,
            self.travel_model.unlink,
            cr, user_id, travel_id, context=context
        )

    def test_create_travel_bad_date(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        self.assertRaises(
            except_orm,
            self.travel_model.create,
            cr, uid,
            dict(vals, date_start=self.year+'-01-21'),
            context=context
        )

    def test_write_travel_bad_date(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        travel_id = self.travel_model.create(cr, uid, vals, context=context)
        self.assertRaises(
            except_orm,
            self.travel_model.write,
            cr, uid, travel_id,
            dict(vals, date_start=self.year+'-01-21'),
            context=context
        )
