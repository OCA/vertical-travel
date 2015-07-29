# -*- encoding: utf-8 -*-
# #############################################################################
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

from openerp.osv import fields, orm


class travel_journey_order_form(orm.TransientModel):
    _name = "travel.journey.order.form"
    _description = "Travel Journey Order Form"
    _columns = {
        'travel_id': fields.many2one(
            'travel.travel', string="Travel", required=True),
        'journey_id': fields.many2one(
            'travel.journey', string="Journey", required=True),
    }

    def print_report(self, cr, uid, ids, data, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]

        assert len(ids) == 1, 'Expected a single record'

        wizard = self.browse(cr, uid, ids, context=context)[0]
        journey = wizard.journey_id
        data['ids'] = [journey.id]
        data['model'] = ['travel.journey']

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'travel.journey.order.webkit',
            'datas': data,
        }

    def update_journey_domain(self, cr, uid, ids, travel_id, context=None):
        travel_pool = self.pool.get('travel.travel')
        travel = travel_pool.browse(cr, uid, travel_id, context=context)
        return {
            'domain': {
                'budgets': [('id', 'in', [j.id for j in travel.journey_ids])],
            }
        }
