from odoo import models, fields, api, _

class kelas(models.Model):
    _name = 'nilai.kelas'
    _description = 'class untuk menyimpan data kelas yang dibuka pada suatu semester'

    name = fields.Char(compute='_compute_name', store=True, recursive=True)
    semester = fields.Selection([('Genap', 'Genap'),
                                 ('Gasal', 'Gasal')],
                                'Semester', required=True, readonly=True,
                                default='Genap', states={'draft': [('readonly', False)]})
    tahun = fields.Char("Tahun", size=15, default="2021/2022", required=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Approved'),
                              ('canceled', 'Canceled')], 'State', required=True,
                             readonly=True, default='draft')
    mk_id = fields.Many2one('nilai.matakuliah', string='Mata Kuliah', readonly=True, ondelete="cascade", required=True,
                            states={'draft': [('readonly', False)]},
                            domain="[('state', '=', 'done')]")
    line_ids = fields.One2many('nilai.kelas.lines', 'kelas_id', string='Nilai', readonly=True,
                               states={'draft': [('readonly', False)]})
    _sql_constraints = [
        ('name_unik', 'unique(mk_id, semester, tahun)', _('The class is already exist for the semester!'))]

    @api.depends('mk_id.name', 'semester', 'tahun')
    def _compute_name(self):
        for s in self:
            s.name = '%s - %s - %s' % (s.mk_id.name, s.semester, s.tahun)

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    def action_wiz_nilai(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard Nilai Kelas'),
            'res_model': 'wiz.nilai.kelas',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

class kelas_lines(models.Model):
    _name = 'nilai.kelas.lines'
    _description = 'class untuk menyimpan data nilai suatu kelas'

    kelas_id = fields.Many2one('nilai.kelas', string='Kelas', ondelete="cascade")
    mhs_id = fields.Many2one('nilai.mahasiswa', string='Mahasiswa', ondelete="restrict")
    grade = fields.Selection([('A', 'A'),
                              ('B+', 'B+'),
                              ('B', 'B'),
                              ('C+', 'C+'),
                              ('C', 'C'),
                              ('D', 'D'),
                              ('E', 'E')])
    _sql_constraints = [('name_unik', 'unique(kelas_id, mhs_id)', _('The student is already exist!'))]
