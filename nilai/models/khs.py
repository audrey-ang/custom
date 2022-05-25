from odoo import models, fields, api, _

class nilai(models.Model):  # inherit dari Model
    # Attribute dari class Mahasiswa
    _name = 'nilai.khs'
    _description = 'class untuk view KHS mahasiswa Infor UK Petra'

    # Attribute Fields
    # Attribute fields nama perlu di compute supaya terlihat objectnya KHS / ...
    name = fields.Char(compute="_compute_name", store=True, recursive=True)
    semester = fields.Selection(
                              [('genap', 'Genap'),
                               ('gasal', 'Gasal')], 'Semester', required=True, readonly=True,
                                default='Genap', states={'draft': [('readonly', False)]})
    ips = fields.Float('IPS', digits=(3,2), compute="_compute_ips", store=True, default=0)
    tahun = fields.Char('Tahun', size=20, default="2021/2022", required=True, readonly=True,
                        states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # Attribute Fields refer to Model Mahasiswa
    mhs_id = fields.Many2one('nilai.mahasiswa', string='Mahasiswa', readonly=True, ondelete="cascade",
                             states={'draft': [('readonly', False)]},
                             domain="[('state', '=', 'done'), ('status', '=', 'aktif')]")

    # Attribute Fields 1:M detailkhs_ids supaya bs ambil dari detailkhs.py, s -> ditambahin karena penamaan default di odoo 1:M
    detailkhs_ids = fields.One2many('nilai.detailkhs', 'khs_id', string='Nilai')

    # Attribute tmp untuk menampung total detailKHS tiap semesternya
    total_tmp = fields.Float(digits=(3,2), store=True, recursive=True)
    total_sks_tmp = fields.Integer(store=True, recursive=True)

    # Constraint supaya unique namenya
    _sql_constraints = [('khs_unik', 'unique(semester, tahun)', _('KHS must be unique!'))]

    # Def untuk di khs_views supaya statesnya dapat diupdate
    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    # Attribute fields nama perlu di compute supaya terlihat objectnya KHS / ...
    @api.depends('mhs_id.name', 'semester', 'tahun')
    def _compute_name(self):
        for s in self:
            s.name = '%s - %s - %s' % (s.mhs_id.name, s.semester, s.tahun)

    # @api.depends('detailkhs_ids.total')
    # def _compute_ips(self):
    #     for nilai in self:
    #         val = {
    #             "total_tmp": 0,
    #             "total_sks_tmp": 0,
    #             "ips": 0,
    #         }
    #     for rec in nilai.detailkhs_ids:
    #         val["total_tmp"] += rec.total
    #         val["total_sks_tmp"] += rec.nilai_sks
    #         val["ips"] = val["total_tmp"] / val["total_sks_tmp"]
    #     nilai.update(val)

    # @api.model
    # def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=none):


