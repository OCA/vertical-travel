# -*- encoding: utf-8 -*-
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

from openerp.tests import common
from datetime import date

class Test_travel(common.TransactionCase):

    def setUp(self):
        """*****setUp*****"""
        super(Test_travel, self).setUp()
        cr, uid = self.cr, self.uid
        self.travel_travel = self.registry('travel.travel')
        self.res_country_state_city = self.registry('res.country.state.city')
        self.travel_passenger = self.registry('travel.passenger')
        self.travel_journey = self.registry('travel.journey')
        self.res_partner = self.registry('res.partner')


        self.city_id = self.res_country_state_city.search(cr, uid, [('code', '=', 'test')])
        self.journey_id = self.travel_journey.search(cr, uid, [('id', '=', 1)])
        self.partner_id = self.res_partner.search(cr, uid, [('id', '=', 1)])

        # create id journey
        self.travel_journey_id = self.travel_journey.create(cr, uid, {
            'from': self.city_id[0],
            'to': self.city_id[0],
            'airport_from': self.res_partner.search(cr, uid, [('airport', '=', 'True')])[0],
            'airport_to': self.res_partner.search(cr, uid, [('airport', '=', 'True')])[0],
            'airline': self.res_partner.search(cr, uid, [('airline', '=', 'True')])[0],
            'passenger_id': self.travel_passenger_id,
        }, context=None)

         # create passenger
        self.travel_passenger_id = self.travel_passenger.create(cr, uid, {
            'name': self.partner_id[0],
            'date': date.today(),
            'journey_ids': [],
            'travel_id': self.travel_id,
        })

        # create id travel
        self.travel_id = self.travel_travel.create(cr, uid, {
            'name': 'This is a travel test',
            'city_id': self.city_id[0],
            'date_start': date.today(),
            'date_start': date.today(),
            'passenger_ids': '[]',
        }, context=None)



    def test_travel(self):
        """
        I check if the simple note, the title and the content were created as
        expected.
        """
        cr, uid = self.cr, self.uid
        travel = self.travel_travel.browse(cr, uid, self.travel_id, context=None)
        self.assertEquals(travel.name, 'This is a travel test')



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
