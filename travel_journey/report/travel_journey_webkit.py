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

from openerp.report import report_sxw
from openerp.addons.report_webkit.webkit_report import WebKitParser


class travel_journey_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(travel_journey_report, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'who': self._get_signer,
            'signer': self._get_signer,
            'passenger': self._get_passenger,
        })

    def _get_signer(self, journey):
        try:
            return self.localcontext['user'].name_get()[0][1]
        except (KeyError, IndexError):
            return ''

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


WebKitParser(
    name='report.travel.journey.order.webkit',
    table='travel.journey',
    rml='addons/travel_journey/report/travel_passenger.mako',
    parser=travel_journey_report,
    header='external',
)
