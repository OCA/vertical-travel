# -*- encoding: utf-8 -*-
##############################################################################
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
##############################################################################

import logging
from openerp.report import report_sxw
from openerp.addons.travel_journey.report import travel_journey_webkit

_logger = logging.getLogger(__name__)


class travel_journey_report(travel_journey_webkit.travel_journey_report):

    def __init__(self, cr, uid, name, context=None):
        super(travel_journey_report, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'who': self._get_who,
        })

    def _get_who(self, journey):
        cr, uid, context = self.cr, self.uid, self.localcontext
        employee_pool = self.pool.get('hr.employee')
        employee_ids = employee_pool.search(
            cr, uid, [('user_id', '=', uid)], context=context)
        try:
            return next(
                employee.department_id.name_get()[0][1]
                for employee in
                employee_pool.browse(cr, uid, employee_ids, context=context)
                if employee.department_id)
        except (StopIteration, IndexError):
            _logger.warn('Unable to get department from user. Using name.')
            return super(travel_journey_report, self)._get_who()

    def _get_passenger(self, journey):
        """This function allows to get the name and job name for the passenger.

        :param journey: travel.journey record
        :return: html string with name and the job of the passenger.
        """
        user_object = self.pool['res.users']
        employee_object = self.pool['hr.employee']
        try:
            passenger_name = journey.passenger_id.partner_id.name or ''
            # Get job name for passenger
            partner_id = journey.passenger_id.partner_id.id
            user_ids = user_object.search(
                self.cr, self.uid, [('partner_id', '=', partner_id)])
            employee_ids = employee_object.search(
                self.cr, self.uid, [('user_id', 'in', user_ids)])
            job_id = employee_object.browse(
                self.cr, self.uid, employee_ids[0]).job_id
            job_name = ''
            if job_id:
                job_name = job_id.name

        except AttributeError:
            passenger_name, job_name = '', ''
        return """\
      <table width="100%%">
        <tr>
          <td class="field_input">
            %s, &nbsp; %s
          </td>
        </tr>
      </table>
""" % (passenger_name, job_name)

report_sxw.report_sxw(
    name='report.travel.journey.hr.order.webkit',
    table='travel.journey',
    rml='addons/travel_journey/report/travel_passenger.mako',
    parser=travel_journey_report,
    header='external',
)
