# -*- encoding: utf-8 -*-
###############################################################################
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
###############################################################################

from ..models.res_config import DEFAULT_PASSENGER_LIMIT
from openerp.tests.common import TransactionCase


class TestPassengerConfig(TransactionCase):

    def setUp(self):
        super(TestPassengerConfig, self).setUp()
        self.vals = {
            'basic_passenger_limit': 8,
        }

    def test_passenger_limit(self):
        """Test default passenger limit before and after it is changed"""
        setting_pool = self.env["travel.config.settings"]
        self.assertEqual(
            setting_pool.get_basic_passenger_limit(),
            DEFAULT_PASSENGER_LIMIT,
            "Passenger limit isn't at the default %d" % DEFAULT_PASSENGER_LIMIT
        )
        settings = self.env["travel.config.settings"].create(self.vals)
        settings.set_basic_passenger_limit()
        self.assertEqual(
            settings.get_basic_passenger_limit(),
            self.vals['basic_passenger_limit'],
            "Passenger limit hasn't been properly changed to %d"
            % self.vals['basic_passenger_limit']
        )
