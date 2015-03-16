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
    'name': 'Partner Airport: Module Data',
    'version': '0.1',
    'category': 'Customer Relationship Management',
    'description': """
Partner Airport: Module Data
============================

Core Data for Partner Airport, is kept as a separate module to overcome the
need to localize core data as well as to avoid long load times.

Contributors
------------
* Sandy Carter (sandy.carter@savoirfairelinux.com)
* El Hadji Dem (elhadji.dem@savoirfairelinux.com)
    """,
    'author': "Savoir-faire Linux,Odoo Community Association (OCA)",
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'depends': ['airport', ],
    'external_dependencies': {},
    'data': [
        'data/airport_data.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'images': [],
}
