# -*- encoding: utf-8 -*-
###############################################################################
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
###############################################################################

from ..report.travel_journey_webkit import travel_journey_report
from openerp.addons.travel_journey.tests.test_journey \
    import test_journey_base


class test_journey_hr_base(test_journey_base):
    def setUp(self):
        super(test_journey_hr_base, self).setUp()
        # To Do: move the following hr part to travel_journey_hr
        # in a seperate unit test
        hr_jobs = self.registry('hr.job')
        job_id = hr_jobs.create(
            self.cr, self.uid, {'name': 't_job_name'}, context=self.context
        )
        employee_object = self.registry('hr.employee')
        employee_object.create(
            self.cr,
            self.uid,
            {'name': 't_employee', 'user_id': self.user_id, 'job_id': job_id},
            context=self.context
        )
        self.passenger_id = self.passenger_model.create(self.cr, self.uid, {
            'partner_id': self.user.partner_id.id,
            'travel_id': self.travel_id,
        }, context=self.context)
        city_id = self.city_model.create(self.cr, self.uid, {
            'city': 'test_city'
        }, context=self.context)
        self.vals = {
            'origin': city_id,
            'destination': city_id,
            'departure': '2014-03-12',
            'passenger_id': self.passenger_id,
        }


class test_journey_hr(test_journey_hr_base):

    def test_get_passenger(self):
        """Test _get_passenger return message."""
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        journey_id = self.journey_model.create(cr, uid, vals, context=context)
        journey_rec = self.journey_model.browse(
            cr, uid, journey_id, context=context)
        report = travel_journey_report(cr, uid, '', context=context)
        expected_return = u"""      <table width="100%">
        <tr>
          <td class="field_input">
            t_name, &nbsp; t_job_name
          </td>
        </tr>
      </table>
"""
        self.assertEqual(report._get_passenger(journey_rec), expected_return)
