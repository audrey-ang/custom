from odoo import models, fields, api, _


class wizkelas(models.TransientModel):
    _name = 'wiz.nilai.kelas'
    _description = 'class untuk menyimpan data kelas dan nilai'

    # Field
    semester = fields.Selection(related='kelas_id.semester')
    tahun = fields.Char(related='kelas_id.tahun')

    # Related field
    mk_id = fields.Many2one(related='kelas_id.mk_id')
    kelas_id = fields.Many2one('nilai.kelas', String='Kelas')
    line_ids = fields.One2many('wiz.nilai.kelas.lines', 'wiz_header_id', string='Nilai')

    @api.model
    def default_get(self,
                    fields_list):  # ini adalah common method, semacam constructor, akan dijalankan saat create object. Ini akan meng-overwrite default_get dari parent
        res = super(wizkelas, self).default_get(fields_list)
        # res  merupakan dictionary beserta value yang akan diisi, yang sudah diproses di super class (untuk create record baru)
        res['kelas_id'] = self.env.context['active_id']
        return res

    @api.onchange('kelas_id')
    def onchange_kelas_id(self):
        if not self.kelas_id:
            return
        vals = []
        line_ids = self.env['wiz.nilai.kelas.lines']
        for rec in self.kelas_id.line_ids:
            line_ids += self.env['wiz.nilai.kelas.lines'].new({
                'wiz_header_id': self.id,
                'mhs_id': rec.mhs_id.id,
                'ref_kelas_lines_id': rec.id
            })

    def action_confirm(self):
        for rec in self.line_ids:
            rec.ref_kelas_lines_id.grade = rec.grade

class kelas_lines_wiz(models.TransientModel):
    _name = 'wiz.nilai.kelas.lines'
    _description = 'class untuk menyimpan data nilai suatu kelas'

    wiz_header_id = fields.Many2one('wiz.nilai.kelas', string='Kelas')
    mhs_id = fields.Many2one('nilai.mahasiswa', string='Mahasiswa', ondelete="restrict")
    ref_kelas_lines_id = fields.Many2one('nilai.kelas.lines')
    grade = fields.Selection([('A', 'A'),
                              ('B+', 'B+'),
                              ('B', 'B'),
                              ('C+', 'C+'),
                              ('C', 'C'),
                              ('D', 'D'),
                              ('E', 'E')])

    def action_wiz_nilai(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard Nilai Kelas'),
            'res_model': 'wiz.nilai.kelas',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }
