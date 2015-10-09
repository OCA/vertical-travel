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

{
    'name': 'Travel Journey',
    'version': '8.0.0.1.0',
    'author': "Savoir-faire Linux,Odoo Community Association (OCA)",
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'category': 'Customer Relationship Management',
    'summary': 'Starting point and destinations of Travel',
    'description': """
Travel journey
==============
This module allows to add a starting point and destination to a travel.

Contributors
------------
* Sandy Carter (sandy.carter@savoirfairelinux.com)
* El Hadji Dem (elhadji.dem@savoirfairelinux.com)
* Joao Alfredo Gama Batista (joao.gama@savoirfairelinux.com)
""",
    'depends': [
        'travel',
        'product',  # for product.uom in baggage weight
        'hr',
    ],
    'data': [
        'views/travel_passenger_view.xml',
        'views/travel_journey_view.xml',
        'data/travel_journey_data.xml',
        'security/ir.model.access.csv',
        'wizard/travel_journey_import_view.xml',
        'wizard/travel_summary_view.xml',
        'views/travel_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
}
