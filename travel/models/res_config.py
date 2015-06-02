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

from openerp import fields, models, api

DEFAULT_PASSENGER_LIMIT = 10


class TravelConfiguration(models.TransientModel):
    """Configuration of travel modules

    Set the limit of passengers non-managers can put on a travel
    """
    _name = 'travel.config.settings'
    _inherit = 'res.config.settings'

    @api.model
    def get_basic_passenger_limit(self):
        """Return set passenger limit if it set, otherwise get default"""
        limit = DEFAULT_PASSENGER_LIMIT
        try:
            limit = self.env["ir.config_parameter"].get_param(
                "travel.basic_passenger_limit"
            )
            limit = int(limit) or DEFAULT_PASSENGER_LIMIT
        finally:
            return limit

    @api.one
    def set_basic_passenger_limit(self):
        """Set passenger limit in config params"""
        self.env["ir.config_parameter"].set_param(
            "travel.basic_passenger_limit",
            self.basic_passenger_limit or DEFAULT_PASSENGER_LIMIT
        )

    basic_passenger_limit = fields.Integer(
        'Basic Passenger Limit',
        default=lambda self: self.get_basic_passenger_limit(),
        help='Limit number of passengers to organize travels by non-managers.'
    )
