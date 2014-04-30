# -*- encoding: utf-8 -*-
################################################################################
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
################################################################################

from openerp.tests.common import TransactionCase


class test_passenger(TransactionCase):

    def setUp(self):
        super(test_passenger, self).setUp()
        # Clean up registries
        self.registry('ir.model').clear_caches()
        self.registry('ir.model.data').clear_caches()
        # Get registries
        self.user_model = self.registry("res.users")
        self.partner_model = self.registry("res.partner")
        self.travel_model = self.registry("travel.travel")
        self.passenger_model = self.registry("travel.passenger")
        # Get context
        self.context = self.user_model.context_get(self.cr, self.uid)
        # Create values for test, travel and partner also created
        self.travel_id = self.travel_model.create(self.cr, self.uid, {
            'name': 'test_travel',
            'date_start': '2014-03-01',
            'date_stop': '2014-03-12',
        }, context=self.context)
        self.partner_id = self.partner_model.create(
            self.cr, self.uid, {'name': 'test_partner'}, context=self.context)
        self.vals = {
            'partner_id': self.partner_id,
            'travel_id': self.travel_id,
        }

    def test_create_passenger(self):
        self.passenger_model.create(
            self.cr, self.uid, self.vals, context=self.context)

    def test_name_get(self):
        passenger_id = self.passenger_model.create(
            self.cr, self.uid, self.vals, context=self.context)
        self.assertEquals(self.passenger_model.name_get(
            self.cr, self.uid, passenger_id,
            context=self.context)[0][1], 'test_partner')

    def test_name_search(self):
        passenger_id = self.passenger_model.create(
            self.cr, self.uid, self.vals, context=self.context)
        self.assertEquals(passenger_id, self.passenger_model.name_search(
            self.cr, self.uid, name='test_partner',
            context=self.context)[0][0])

    def test_call_action_passenger_form_view(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        passenger_id = self.passenger_model.create(
            cr, uid, vals, context=context)
        self.assertTrue(
            self.passenger_model.action_passenger_form_view(
                cr, uid, passenger_id, context=context)
        )

    def test_call_on_change_partner_id(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        passenger_id = self.passenger_model.create(
            cr, uid, vals, context=context)
        self.assertIsNotNone(
            self.passenger_model.on_change_partner_id(
                cr, uid, passenger_id, uid, context=context)
        )
