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

from openerp.tests.common import TransactionCase
from openerp.osv.orm import except_orm
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT
from openerp.tools.translate import _

from openerp.addons.travel_journey.report.travel_journey_webkit \
    import travel_journey_report


class test_journey(TransactionCase):

    def setUp(self):
        super(test_journey, self).setUp()
        # Clean up registries
        self.registry('ir.model').clear_caches()
        self.registry('ir.model.data').clear_caches()
        # Get registries
        self.user_model = self.registry("res.users")
        self.partner_model = self.registry("res.partner")
        self.travel_model = self.registry("travel.travel")
        self.passenger_model = self.registry("travel.passenger")
        self.journey_model = self.registry("travel.journey")
        self.city_model = self.registry("res.better.zip")
        # Get context
        self.context = self.user_model.context_get(self.cr, self.uid)
        # Create values for test, travel and partner also created
        self.travel_id = self.travel_model.create(self.cr, self.uid, {
            'name': 'test_travel',
            'date_start': '2014-03-01',
            'date_stop': '2014-03-12',
        }, context=self.context)
        user_object = self.registry('res.users')
        user_id = user_object.create(
            self.cr, self.uid, {'name': 't_name', 'login': 't_login'}
        )
        user = user_object.browse(
            self.cr, self.uid, user_id, context=self.context
        )
        hr_jobs = self.registry('hr.job')
        job_id = hr_jobs.create(
            self.cr, self.uid, {'name': 't_job_name'}, context=self.context
        )
        employee_object = self.registry('hr.employee')
        employee_object.create(
            self.cr,
            self.uid,
            {'name': 't_employee', 'user_id': user_id, 'job_id': job_id},
            context=self.context
        )
        self.passenger_id = self.passenger_model.create(self.cr, self.uid, {
            'partner_id': user.partner_id.id,
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

    def test_create_journey(self):
        self.journey_model.create(
            self.cr, self.uid, self.vals, context=self.context)

    def test_create_journey_return(self):
        self.journey_model.create(
            self.cr, self.uid,
            dict(self.vals, is_return=True, return_departure='2014-03-31'),
            context=self.context)

    def test_import_journey(self):
        self.journey_model.create(
            self.cr, self.uid, self.vals, context=self.context)
        journey_import_model = self.registry("travel.journey.import")

        # Try with without a passenger_id
        wizard_bad = journey_import_model.create(self.cr, self.uid, {
            'travel_id': self.travel_id,
            'cur_passenger_id': self.passenger_id,
        }, context=self.context)
        self.assertRaises(
            except_orm,
            journey_import_model.data_import,
            self.cr, self.uid, [wizard_bad], context=self.context)

        # Try with with a passenger_id
        partner_id = self.partner_model.create(
            self.cr, self.uid, {'name': 'test_partner'}, context=self.context)
        import_passenger_id = self.passenger_model.create(self.cr, self.uid, {
            'partner_id': partner_id,
            'travel_id': self.travel_id,
        }, context=self.context)
        wizard_good = journey_import_model.create(self.cr, self.uid, {
            'travel_id': self.travel_id,
            'cur_passenger_id': self.passenger_id,
            'passenger_id': import_passenger_id,
        }, context=self.context)
        journey_import_model.data_import(
            self.cr, self.uid, [wizard_good], context=self.context)

    def test_estimate_datetime(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        journey_id = self.journey_model.create(
            cr, uid,
            dict(vals, departure=None, arrival='2014-05-01'),
            context=context)
        dt = self.journey_model._estimate_datetime(
            cr, uid, journey_id, 'date_start', context=context)
        date = self.journey_model._estimate_date(
            cr, uid, journey_id, 'date_start', context=context)
        time = self.journey_model._estimate_time(
            cr, uid, journey_id, 'date_start', context=context)
        self.assertEqual(dt[journey_id].strftime(DEFAULT_SERVER_DATE_FORMAT),
                         '2014-03-01')
        self.assertEqual(date[journey_id], '2014-03-01')
        self.assertEqual(time[journey_id], '00:00:00')
        journey_id = self.journey_model.create(cr, uid, vals, context=context)
        dt = self.journey_model._estimate_datetime(
            cr, uid, journey_id, 'date_stop', context=context)
        date = self.journey_model._estimate_date(
            cr, uid, journey_id, 'date_stop', context=context)
        time = self.journey_model._estimate_time(
            cr, uid, journey_id, 'date_stop', context=context)
        self.assertEqual(dt[journey_id].strftime(DEFAULT_SERVER_DATE_FORMAT),
                         '2014-03-12')
        self.assertEqual(date[journey_id], '2014-03-12')
        self.assertEqual(time[journey_id], '00:00:00')

    def test_on_change(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        journey_id = self.journey_model.create(cr, uid, vals, context=context)
        new_city_id = self.city_model.create(self.cr, self.uid, {
            'city': 'new_test_city'
        }, context=self.context)
        res = self.journey_model.on_change_return(
            cr, uid, journey_id, key='return_destination',
            location=new_city_id, context=context)
        self.assertEqual(res['value']['return_destination'], new_city_id)
        res = self.journey_model.on_change_times(
            cr, uid, journey_id, departure='2014-03-01', arrival='2014-03-12',
            return_trip=False, context=context)
        self.assertEqual(res, {})
        res = self.journey_model.on_change_times(
            cr, uid, journey_id, departure='2014-03-12', arrival='2014-03-01',
            return_trip=False, context=context)
        self.assertIn('warning', res)

    def test_checks(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        journey_id = self.journey_model.create(cr, uid, vals, context=context)
        self.assertTrue(self.journey_model.check_date_exists(
            cr, uid, journey_id, context=context))
        self.assertTrue(self.journey_model.check_date_exists_return(
            cr, uid, journey_id, context=context))
        self.assertTrue(self.journey_model.check_date(
            cr, uid, journey_id, context=context))
        self.assertTrue(self.journey_model.check_date_return(
            cr, uid, journey_id, context=context))
        self.assertTrue(self.journey_model.check_uom(
            cr, uid, journey_id, context=context))

    def test_company_get(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        journey_id = self.journey_model.create(cr, uid, vals, context=context)
        self.assertEqual(self.journey_model.company_get(
            cr, uid, [journey_id], context=context), _("N/A"))

    def test_inv_estimate_date(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        journey_id = self.journey_model.create(cr, uid, vals, context=context)
        self.journey_model._inv_estimate_date(
            cr, uid, journey_id,
            field_name='date_start', val='2014-03-05',
            arg=None, context=context)
        self.journey_model._inv_estimate_date(
            cr, uid, journey_id,
            field_name='date_stop', val='2014-03-10',
            arg=None, context=context)
        journey_id = self.journey_model.create(
            cr, uid,
            dict(vals, departure=None, arrival='2014-05-01'),
            context=context)
        self.journey_model._inv_estimate_date(
            cr, uid, journey_id,
            field_name='date_start', val='2014-03-05',
            arg=None, context=context)
        self.journey_model._inv_estimate_date(
            cr, uid, journey_id,
            field_name='date_stop', val='2014-03-10',
            arg=None, context=context)

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
