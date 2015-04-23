# -*- encoding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2010 Savoir-faire Linux
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
###############################################################################

import copy

from openerp.tests.common import TransactionCase
from .test_travel import TRAVEL_VALS


class TestPassenger(TransactionCase):

    def setUp(self):
        """Create values for test, travel and partner also created"""
        super(TestPassenger, self).setUp()

        self.travel_vals = copy.copy(TRAVEL_VALS)
        self.partner_vals = {'name': 'test_partner'}

        self.travel = self.env['travel.travel'].create(self.travel_vals)
        self.partner = self.env['res.partner'].create(self.partner_vals)

        self.vals = {
            'partner_id': self.partner.id,
            'travel_id': self.travel.id,
        }

        self.passenger = self.env['travel.passenger'].create(self.vals)

    def test_name_get(self):
        """Test name_get of passenger"""
        self.assertEquals(
            self.passenger.name_get()[0][1],
            self.partner_vals['name'],
        )

    def test_name_search(self):
        """Test name_search of passenger"""
        self.assertEquals(
            self.partner.id,
            self.env['res.partner'].name_search(name='test_partner')[0][0],
        )

    def test_call_action_passenger_form_view(self):
        """Test that action_passenger_form_view returns the proper
        default dates in context
        """
        context = self.passenger.action_passenger_form_view()['context']
        self.assertEqual(
            context.get('default_date_start'),
            self.travel_vals.get('date_start'),
            "Default start date for passenger doesn't match that of the travel"
        )
        self.assertEqual(
            context.get('default_date_stop'),
            self.travel_vals.get('date_stop'),
            "Default stop date for passenger doesn't match that of the travel"
        )

    def test_call_on_change_partner_id(self):
        """Test call of placeholder on_change_partner_id"""
        self.assertIsNotNone(self.passenger.on_change_partner_id())
