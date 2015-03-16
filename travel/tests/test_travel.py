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
from openerp import exceptions
import time
import copy

YEAR = str(time.localtime(time.time())[0])
TRAVEL_VALS = {
    'name': 'This is a test travel name',
    'date_start': YEAR + '-01-01',
    'date_stop': YEAR + '-01-14',
}


class TestTravel(TransactionCase):

    def setUp(self):
        """Create values for test, travel and partner also created"""
        super(TestTravel, self).setUp()
        self.year = copy.copy(YEAR)
        self.vals = copy.copy(TRAVEL_VALS)
        self.travel = self.env['travel.travel'].create(self.vals)

    def test_write_travel(self):
        """Test basic write of date_stop on travel.travel"""
        self.travel.write({'date_stop': self.year + '-01-21'})

    def test_unlink_travel(self):
        """Test basic unlink of travel.travel"""
        self.travel.unlink()

    def test_unlink_non_draft_travel(self):
        """Test basic unlink of travel.travel after it has been opened"""
        self.travel.travel_open()
        with self.assertRaises(
            exceptions.Warning,
            msg="Warning wasn't raised when a non-draft travel was unlinked"
        ):
            self.travel.unlink()

    def test_change_state_travel(self):
        """Test workflow of travel.travel"""
        states = {
            'open': 'travel_open',
            'booking': 'travel_book',
            'reserved': 'travel_reserve',
            'confirmed': 'travel_confirm',
            'done': 'travel_close',
        }
        for state, func in states.iteritems():
            self.assertTrue(
                getattr(self.travel, func)(),
                "Failure while calling %s" % func
            )
            self.assertEqual(
                self.travel.state,
                state,
                "Travel state did not properly update to %s after calling %s"
                % (state, func)
            )

    def test_travel_too_many_passengers(self):
        """Test travel if it can only be modified by manager

        First with no passengers, after with more than limit
        """
        self.assertFalse(self.travel.is_manager_only()[self.travel.id])
        vals = dict(self.vals, passenger_ids=[])
        for i in xrange(12):
            partner_id = self.env['res.partner'].create(
                {'name': 'test_partner_%d' % i}
            ).id
            vals["passenger_ids"].append(tuple([0, 0, {
                "partner_id": partner_id,
            }]))
        self.travel.write(vals)
        self.assertTrue(self.travel.is_manager_only()[self.travel.id])

    def test_create_travel_too_many_passengers(self):
        """Test creation of travel with too many passengers using basic user"""
        user = self.env['res.users'].create({
            'login': 'test',
            'name': 'test',
            'groups_id': [(4, self.ref('travel.group_basic_travel_user'))],
        })
        vals = dict(self.vals, passenger_ids=[])
        for i in xrange(12):
            partner_id = self.env['res.partner'].create(
                {'name': 'test_partner_%d' % i}
            ).id
            vals["passenger_ids"].append(tuple([0, 0, {
                "partner_id": partner_id,
            }]))
        with self.assertRaises(
            exceptions.Warning,
            msg="Warning wasn't raised when a non-manager tried to add too "
                "many passengers to travel during creation"
        ):
            self.travel.sudo(user).create(vals)

    def test_write_travel_too_many_passengers(self):
        """Test write of travel with too many passengers using basic user"""
        user = self.env['res.users'].create({
            'login': 'test',
            'name': 'test',
            'groups_id': [(4, self.ref('travel.group_basic_travel_user'))],
        })
        vals = dict(passenger_ids=[])
        for i in xrange(12):
            partner_id = self.env['res.partner'].create(
                {'name': 'test_partner_%d' % i}
            ).id
            vals["passenger_ids"].append(tuple([0, 0, {
                "partner_id": partner_id,
            }]))
        with self.assertRaises(
            exceptions.Warning,
            msg="Warning wasn't raised when a non-manager tried to add too "
                "many passengers to travel during write"
        ):
            self.travel.sudo(user).write(vals)
        self.travel.write(vals)
        with self.assertRaises(
            exceptions.Warning,
            msg="Warning wasn't raised when a non-manager tried to write on a "
                "travel with too many passengers"
        ):
            self.travel.sudo(user).write({'name': 'changed'})

    def test_unlink_travel_too_many_passengers(self):
        """Test unlink of travel with too many passengers using basic user"""
        user = self.env['res.users'].create({
            'login': 'test',
            'name': 'test',
            'groups_id': [(4, self.ref('travel.group_basic_travel_user'))],
        })
        vals = dict(self.vals, passenger_ids=[])
        for i in xrange(12):
            partner_id = self.env['res.partner'].create(
                {'name': 'test_partner_%d' % i}
            ).id
            vals["passenger_ids"].append(tuple([0, 0, {
                "partner_id": partner_id,
            }]))
        self.travel.write(vals)
        with self.assertRaises(
            exceptions.Warning,
            msg="Warning wasn't raised when a non-manager tried to add too "
                "many passengers to travel during unlink"
        ):
            self.travel.sudo(user).unlink()

    def test_create_travel_bad_date(self):
        """Test creation of travel with bad date"""
        with self.assertRaises(
            exceptions.ValidationError,
            msg="Warning wasn't raised when creating a travel with start date "
                "later than stop date"
        ):
            self.travel.create(
                dict(self.vals, date_start=self.year + '-01-21')
            )

    def test_write_travel_bad_date(self):
        """Test write of a bad date on travel"""
        with self.assertRaises(
            exceptions.ValidationError,
            msg="Warning wasn't raised when setting a travel with start date "
                "later than stop date"
        ):
            self.travel.write(
                dict(self.vals, date_start=self.year + '-01-21'),
            )
