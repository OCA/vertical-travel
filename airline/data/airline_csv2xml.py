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
##############################################################################

import csv

csvFile = 'airline_data.csv'
xmlFile = 'airline_data.xml'

csvData = csv.reader(open(csvFile))
xmlData = open(xmlFile, 'w')
xmlData.write('<?xml version="1.0" encoding="utf-8"?>' + "\n")
xmlData.write('<openerp>' + "\n")
# there must be only one top-level tag
xmlData.write('  '+'<data noupdate="1">' + "\n")

rowNum = 0
for row in csvData:
    if rowNum == 0:
        tags = row
        # replace spaces w/ underscores in tag names
        for i in range(len(tags)):
            tags[i] = tags[i].replace(' ', '_')
    else:
        xmlData.write('<record forcecreate="True" id="' + str(rowNum) + '" model="res.partner">' + "\n")
        for i in range(len(tags)):
            xmlData.write('    ' + '<field name="' + tags[i] + '">' + row[i] + '</field>' + "\n")
        xmlData.write('</record>' + "\n")
    rowNum += 1

xmlData.write('  '+'</data>' + "\n")
xmlData.write('</openerp>' + "\n")
xmlData.close()