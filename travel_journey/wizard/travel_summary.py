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

import base64
from xlwt import Workbook, Formula, Font, XFStyle, Alignment, Borders, Pattern
from StringIO import StringIO

from openerp.osv import fields, orm
from openerp.tools.translate import _


class Cell(object):

    def __init__(self, text, font, alignment, border, pattern,
                 number_format_str='General', width=0x0E00, ):
        self.text = text
        self.font = font
        self.alignment = alignment
        self.border = border
        self.pattern = pattern
        self.style = XFStyle()
        self.style.font = self.font
        self.style.alignment = self.alignment
        self.style.borders = self.border
        self.style.pattern = self.pattern
        self.style.num_format_str = number_format_str
        self.width = width


class Column(Cell):
    title_fnt = Font()
    title_fnt.name = 'Calibri'
    title_fnt.bold = True
    title_fnt.height = 12 * 20  # font size 12

    obj_fnt = Font()
    obj_fnt.name = 'Calibri'
    obj_fnt.height = 12 * 20  # font size 12

    title_aln = Alignment()
    title_aln.horz = Alignment.HORZ_CENTER
    title_aln.vert = Alignment.VERT_CENTER
    title_aln.wrap = Alignment.WRAP_AT_RIGHT

    title_ptn = Pattern()
    title_ptn.pattern = Pattern.SOLID_PATTERN
    title_ptn.pattern_fore_colour = 0x2C

    def __init__(self, text, left_border=False, right_border=False,
                 use_pattern=False, width=0x0E00, func=lambda obj: ""):
        super(Column, self).__init__(
            text, self.title_fnt, self.title_aln, Borders(),
            self.title_ptn, width=width
        )
        self.obj_style = XFStyle()
        self.obj_style.alignment = self.title_aln

        self.obj_style.borders = Borders()
        self.obj_style.borders.left = Borders.HAIR
        self.obj_style.borders.right = Borders.HAIR
        self.obj_style.borders.top = Borders.HAIR
        self.obj_style.borders.bottom = Borders.HAIR
        self.border.left = Borders.HAIR
        self.border.right = Borders.HAIR
        self.border.top = Borders.THICK
        self.border.bottom = Borders.THICK

        if left_border:
            self.obj_style.borders.left = Borders.THICK
            self.border.left = Borders.THICK
        if right_border:
            self.obj_style.borders.right = Borders.THICK
            self.border.right = Borders.THICK

        self.obj_style.font = self.obj_fnt

        if use_pattern:
            self.obj_style.pattern = self.pattern

        self.func = func


class travel_summary(orm.TransientModel):
    _name = "travel.summary"
    _description = "Travel Journey Summary"
    _columns = {
        'travel_id': fields.many2one(
            'travel.travel', string="Travel", required=True),
        'excel_file': fields.binary('Report', readonly=True),
        'export_filename': fields.char('Export Filename', size=128),
    }
    _defaults = {
        'export_filename': lambda self, *a: self._get_filename(*a),
    }

    def _get_filename(self, cr, uid, ids, context=None):
        return _('travel_summary.xls')

    def get_excel_columns(self, context=None):
        return [
            Column(_('#'), left_border=True, width=0x0400),
            Column(_('NAME'), width=0x1000,
                   func=lambda obj: obj.passenger_id.partner_id.name),
            Column(_('CO.'), left_border=True, width=0x0700,
                   func=lambda obj: obj.company_get()),
            Column(_('Departure City'), left_border=True, width=0x1400,
                   func=lambda obj: obj.origin_get()[0].display_name),
            Column(_('Departure Date'),
                   func=lambda obj: obj.departure_date_get()),
            Column(_('Departure Time'),
                   func=lambda obj: obj.departure_time_get()),
            Column(_('Arrival City'), width=0x1400,
                   func=lambda obj: obj.destination_get()[0].display_name),
            Column(_('Arrival Date'),
                   func=lambda obj: obj.arrival_date_get()),
            Column(_('Arrival Time'),
                   func=lambda obj: obj.arrival_time_get()),
            Column(_('TICKET RATE'), left_border=True, use_pattern=True),
            Column(_('COSTS'), use_pattern=True),
            Column(_('TOTAL'), right_border=True, use_pattern=True),
        ]

    def export_excel(self, cr, uid, ids, context=None):
        """Export a journey summary an excel file

        This reopens the current wizard with a download link to the gathered
        data, instead of populating the tree view.
        """
        travel_smry_id = ids[0] if type(ids) is list else ids
        travel_smry_pool = self.pool.get('travel.summary')
        travel_smry = travel_smry_pool.browse(
            cr, uid, travel_smry_id, context=context)
        travel = travel_smry.travel_id
        output = StringIO()
        try:
            workbook = self.produce_summary(cr, uid, travel, context=context)
            workbook.save(output)
            self.write(cr, uid, ids, {
                'excel_file': base64.encodestring(output.getvalue()),
            }, context=context)
        finally:
            output.close()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'travel.summary',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': travel_smry_id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    def produce_summary(self, cr, uid, travel, context=None):

        number_format = _('#,##0.00 [$$-C0C];-#,##0.00 [$$-C0C]')

        total_fnt = Font()
        total_fnt.name = 'Calibri'
        total_fnt.bold = True
        total_fnt.height = 16 * 20  # font size 12

        total_cell_l_style = XFStyle()
        total_cell_l_style.alignment = Column.title_aln
        total_cell_l_style.borders = Borders()
        total_cell_l_style.borders.left = Borders.THICK
        total_cell_l_style.borders.right = Borders.HAIR
        total_cell_l_style.borders.top = Borders.THICK
        total_cell_l_style.borders.bottom = Borders.THICK
        total_cell_l_style.pattern = Column.title_ptn
        total_cell_l_style.num_format_str = number_format
        total_cell_l_style.font = Column.obj_fnt

        total_cell_r_style = XFStyle()
        total_cell_r_style.alignment = Column.title_aln
        total_cell_r_style.borders = Borders()
        total_cell_r_style.borders.left = Borders.HAIR
        total_cell_r_style.borders.right = Borders.THICK
        total_cell_r_style.borders.top = Borders.THICK
        total_cell_r_style.borders.bottom = Borders.THICK
        total_cell_r_style.pattern = Column.title_ptn
        total_cell_r_style.num_format_str = number_format
        total_cell_r_style.font = Column.obj_fnt

        sub_total_cell_label = Cell(
            _(u'SOUS-TOTAL'), Column.title_fnt, Column.title_aln,
            total_cell_l_style.borders, Column.title_ptn)
        total_cell_label = Cell(
            _(u'TOTAL'), total_fnt, Column.title_aln,
            total_cell_r_style.borders, Column.title_ptn, number_format)
        journeys = [j for i in travel.passenger_ids for j in i.journey_ids]
        w = Workbook()
        ws = w.add_sheet(_('Travel Summary'))

        ws.row(2).height = 0x0280
        ws.row(3 + len(journeys)).height = 0x0140
        ws.row(4 + len(journeys)).height = 0x0180
        row = 0
        row += 2

        _excel_columns = self.get_excel_columns(context)
        # Write headers
        for i, col in enumerate(_excel_columns):
            ws.col(i).width = col.width
            ws.write(row, i, col.text, col.style)
        row += 1
        for i, obj in enumerate(journeys):
            ws.write(row + i, 0, i + 1, _excel_columns[0].obj_style)
            for j in xrange(1, len(_excel_columns)):
                ws.write(row + i, j,
                         _excel_columns[j].func(obj),
                         _excel_columns[j].obj_style)

        row += len(journeys)
        rate_index = [i for i, x in enumerate(_excel_columns)
                      if x.text == _('TICKET RATE')][0] - 1
        cost_index = [i for i, x in enumerate(_excel_columns)
                      if x.text == _('COSTS')][0] - 1
        total_index = [i for i, x in enumerate(_excel_columns)
                       if x.text == _('TOTAL')][0] - 1
        # Sub total label
        ws.write_merge(row, row, 0, rate_index,
                       sub_total_cell_label.text,
                       sub_total_cell_label.style)

        # Sub totals
        ws.write(row, rate_index + 1,
                 Formula("SUM(%s%d:%s%d)" % (chr(66 + rate_index), 4,
                                             chr(66 + rate_index), row)),
                 total_cell_l_style)
        ws.write(row, rate_index + 2,
                 Formula("SUM(%s%d:%s%d)" % (chr(66 + cost_index), 4,
                                             chr(66 + cost_index), row)),
                 total_cell_r_style)
        total_top_underline_style = XFStyle()
        total_top_underline_style.borders = Borders()
        total_top_underline_style.borders.top = Borders.THICK
        total_top_underline_style.font = Column.obj_fnt
        # Draw a line above total to close box
        ws.write(row, total_index + 1, "", total_top_underline_style)
        row += 1
        # Total label
        ws.write_merge(row, row, 0, rate_index,
                       total_cell_label.text,
                       total_cell_label.style)
        # Total
        ws.write_merge(row, row, rate_index + 1, total_index,
                       Formula("%s%d+%s%d" % (chr(66 + rate_index), row,
                                              chr(66 + cost_index), row)),
                       total_cell_label.style)

        return w
