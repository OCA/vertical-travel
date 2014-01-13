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
from openerp.osv.orm import browse_record
from datetime import date


class Base_Test_travel(TransactionCase):
    """
    Simple test creating a travel
    This is a base class for travel test cases.
    Inherit from this and setup values.
    """

    def setUp(self, vals={}):
        """
        Setting up travel.
        """
        # Default test values
        self.vals = {'name': 'This is a test travel name',
                     'date_start': date(2013, 11, 14),
                     'date_stop': date(2013, 11, 21),
                     }
        super(Base_Test_travel, self).setUp()
        # Create the city; we're not testing city, so we don't store in self
        res_country_city = self.registry('res.country.city')
        self.vals['city_id'] = res_country_city.create(self.cr, self.uid, {
            'name': 'Test City',
            'country_id': 1, }, context=None)
        # Overwrite vals if needed
        self.vals = dict(self.vals.items() + vals.items())
        # Create the travel object; we will be testing this, so store in self
        travel_travel = self.registry('travel.travel')
        self.travel_id = travel_travel.create(self.cr, self.uid, self.vals, context=None)

    def test_travel(self):
        """
        Checking the travel creation.
        """
        travel_travel = self.registry('travel.travel')
        travel_obj = travel_travel.browse(self.cr, self.uid, self.travel_id, context=None)
        for field in self.vals:
            val = travel_obj[field]
            if type(val) == browse_record:
                self.assertEquals(self.vals[field], val.id,
                                  "IDs for %s don't match: (%i != %i)" %
                                  (field, self.vals[field], val.id))
            else:
                self.assertEquals(str(self.vals[field]), str(val),
                                  "Values for %s don't match: (%s != %s)" %
                                  (field, str(self.vals[field]), str(val)))


class Test_travel_bad(Base_Test_travel):
    """
    Simple test creating a travel, test against bad values
    """
    def setUp(self):
        """
        Setting up travel, then changing the values to test against.
        """
        super(Test_travel_bad, self).setUp()
        # Change vals to something wrong
        self.vals = {'name': 'This is the wrong travel name',
                     'city_id': 0,
                     'date_start': date(1999, 11, 14),
                     'date_stop': date(1999, 11, 21),
                     }

    def test_travel(self):
        """
        Checking the travel creation, assertions should all be false.
        """
        travel_travel = self.registry('travel.travel')
        travel_obj = travel_travel.browse(self.cr, self.uid, self.travel_id, context=None)
        for field in self.vals:
            val = travel_obj[field]
            if type(val) == browse_record:
                self.assertNotEqual(self.vals[field], val.id,
                                    "IDs for %s don't match: (%i != %i)" %
                                    (field, self.vals[field], val.id))
            else:
                self.assertNotEqual(str(self.vals[field]), str(val),
                                    "Values for %s don't match: (%s != %s)" %
                                    (field, str(self.vals[field]), str(val)))

# TODO: uncomment this test after implementation of date checking
#
# class Test_travel_bad_dates(Base_Test_travel):
#     """
#     Testing a date_stop that happens before a date_start
#     """
#
#     def setUp(self, vals={}):
#         """
#         Setting up travel.
#         """
#         vals = {'name': 'This is a test travel with a date stop before the date start',
#                 'date_start': date(2013, 11, 21),
#                 'date_stop': date(2013, 11, 14),
#                 }
#         super(Test_travel_bad_dates, self).setUp(vals)
#
#     def test_travel(self):
#         """
#         Checking the travel dates creation.
#         """
#         travel_travel = self.registry('travel.travel')
#         travel_obj = travel_travel.browse(self.cr, self.uid, self.travel_id, context=None)
#         self.assertLessEqual(travel_obj['date_start'], travel_obj['date_stop'],
#                              "date_stop cannot be before date_start.")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
