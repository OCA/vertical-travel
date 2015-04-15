# -*- encoding: utf-8 -*-
##############################################################################
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
##############################################################################

{
    'name': 'Travel Accommodation',
    'version': '0.1',
    'author': "Savoir-faire Linux,Odoo Community Association (OCA)",
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'category': 'Customer Relationship Management',
    'summary': 'Accommodations on a Travel',
    'description': """
Travel Accommodation
====================
This module adds accommodation management for travels.

Contributors
------------
* Sandy Carter (sandy.carter@savoirfairelinux.com)
""",
    'depends': ['travel', 'product', 'transportation'],
    'external_dependencies': {},
    'data': [
        'res_partner_view.xml',
        'travel_passenger_view.xml',
        'travel_accommodation_view.xml',
        'security/ir.model.access.csv',
        'wizard/travel_accommodation_import_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
}
