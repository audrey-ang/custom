from odoo import models, fields, api, _

class nilai(models.Model):  # inherit dari Model
    # Attribute dari class Mahasiswa
    _name = 'nilai.detailkhs'
    _description = 'class untuk view KHS mahasiswa Infor UK Petra'

    # Attribute Fields
    grade = fields.Selection([('a', 'A'),
                              ('b+', 'B+'),
                              ('b', 'B'),
                              ('c+', 'C+'),
                              ('c', 'C'),
                              ('d', 'D'),
                              ('e', 'E'), ], 'Grade', required=True, readonly=True,
                             states={'draft': [('readonly', False)]})
    total = fields.Float(compute="_compute_total", digits=(3,2), store=True, recursive=True)

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # Attribute Fields refer to Model KHS
    khs_id = fields.Many2one('nilai.khs', string='KHS', readonly=True, ondelete="cascade",
                             states={'draft': [('readonly', False)]},
                             domain="[('state', '=', 'done')]")

    # Attribute Fields refer to Model Mata Kuliah
    mk_id = fields.Many2one('nilai.matakuliah', string='Mata Kuliah', readonly=True, ondelete='cascade',
                            states={'draft': [('readonly', False)]},
                            domain="[('state', '=', 'done'), ('active', '=', 'True')]")

    # Related field ke table Mata Kuliah
    nilai_sks = fields.Integer("SKS", related='mk_id.sks')

    # Constraint supaya unique namenya
    _sql_constraints = [('mk_id_unik', 'unique(mk_id)', _('Mata Kuliah must be unique!'))]

    # Def untuk di khs_views supaya statesnya dapat diupdate
    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('mk_id.kodeMK', 'grade', 'nilai_sks')
    def _compute_total(self):
        for nilai in self:
            val = {
                "total": 0,
            }
            if self.grade == "a":
                val["total"] += (4 * self.nilai_sks)
            elif self.grade == "b+":
                val["total"] += (3.5 * self.nilai_sks)
            elif self.grade == "b":
                val["total"] += (3 * self.nilai_sks)
            elif self.grade == "c+":
                val["total"] += (2.5 * self.nilai_sks)
            elif self.grade == "c":
                val["total"] += (2 * self.nilai_sks)
            elif self.grade == "d":
                val["total"] += (1 * self.nilai_sks)
            else:
                val["total"] += 0
        nilai.update(val)

#
# # @api.model
# # def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=none):
