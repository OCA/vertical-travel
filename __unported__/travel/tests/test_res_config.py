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
        self.settings_model = self.registry("travel.config.settings")
        # Get context
        self.context = self.user_model.context_get(self.cr, self.uid)
        self.vals = {
            'basic_passenger_limit': 8,
        }

    def test_passenger_limit(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        settings_id = self.settings_model.create(
            cr, uid, vals, context=context)
        default = self.settings_model.get_default_basic_passenger_limit(
            cr, uid, settings_id, context=context)
        self.assertEqual(default['basic_passenger_limit'], 10)
        self.settings_model.set_basic_passenger_limit(
            cr, uid, settings_id, context=context)
