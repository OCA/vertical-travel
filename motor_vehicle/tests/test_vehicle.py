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


class Base_Test_vehicle(TransactionCase):
    """
    Simple test creating a motor vehicle
    This is a base class for motor vehicle test cases.
    Inherit from this and setup values.
    """

    def setUp(self, vals={}):
        """
        Setting up motor vehicle.
        """
        # Default test values
        self.vals = {'name': 'This is a test motor vehicle name',
                     }
        super(Base_Test_vehicle, self).setUp()
        # Overwrite vals if needed
        self.vals = dict(self.vals.items() + vals.items())
        # Create the motor_vehicle object; we will be testing this, so store in self
        motor_vehicle = self.registry('motor.vehicle')
        self.vehicle_id = motor_vehicle.create(self.cr, self.uid, self.vals, context=None)

    def test_vehicle(self):
        """
        Checking the motor vehicle creation.
        """
        motor_vehicle = self.registry('motor.vehicle')
        vehicle_obj = motor_vehicle.browse(self.cr, self.uid, self.vehicle_id, context=None)
        for field in self.vals:
            val = vehicle_obj[field]
            if type(val) == browse_record:
                self.assertEquals(self.vals[field], val.id,
                                  "IDs for %s don't match: (%i != %i)" %
                                  (field, self.vals[field], val.id))
            else:
                self.assertEquals(str(self.vals[field]), str(val),
                                  "Values for %s don't match: (%s != %s)" %
                                  (field, str(self.vals[field]), str(val)))


class Test_vehicle_bad(Base_Test_vehicle):
    """
    Simple test creating a motor vehicle, test against bad values
    """
    def setUp(self):
        """
        Setting up motor vehicle, then changing the values to test against.
        """
        super(Test_vehicle_bad, self).setUp()
        # Change vals to something wrong
        self.vals = {
            'name': 'This is the wrong motor vehicle name',
        }

    def test_vehicle(self):
        """
        Checking the motor vehicle creation, assertions should all be false.
        """
        motor_vehicle = self.registry('motor.vehicle')
        vehicle_obj = motor_vehicle.browse(self.cr, self.uid, self.vehicle_id, context=None)
        for field in self.vals:
            val = vehicle_obj[field]
            if type(val) == browse_record:
                self.assertNotEqual(self.vals[field], val.id,
                                    "IDs for %s don't match: (%i != %i)" %
                                    (field, self.vals[field], val.id))
            else:
                self.assertNotEqual(str(self.vals[field]), str(val),
                                    "Values for %s don't match: (%s != %s)" %
                                    (field, str(self.vals[field]), str(val)))


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
