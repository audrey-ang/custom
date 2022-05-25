from odoo import models, fields, api, _

class nilai(models.Model):  # inherit dari Model
    # Attribute dari class Mahasiswa
    _name = 'nilai.mahasiswa'
    _description = 'Class Mahasiswa SIB UK Petra'

    # Attribute Fields
    nrp = fields.Char('NRP', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    name = fields.Char('Mahasiswa', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    status = fields.Selection(
                            [('aktif', 'Aktif'),
                             ('do', 'DO'),
                             ('cuti', 'Cuti Studi'),
                             ('lulus', 'Lulus')], 'Status', required=True, readonly=True, default='draft',
                            states={'draft': [('readonly', False)]})
    ipk = fields.Float('IPK', digits=(3,2), compute="_compute_ipk", store=True, default=0)
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # Attribute Fields 1:M detailkhs_ids supaya bs ambil dari detailkhs.py, s -> ditambahin karena penamaan default di odoo 1:M
    khs_ids = fields.One2many('nilai.khs', 'mhs_id', string='Nilai', ondelete="cascade")

    # Constraint supaya unique namenya
    _sql_constraints = [('name_unik', 'unique(name)', _('Ideas must be unique!'))]

    # Attribute tmp untuk menampung total detailKHS tiap semesternya
    total_tmp = fields.Float(digits=(3, 2), store=True, recursive=True)
    total_sks_tmp = fields.Integer(store=True, recursive=True)

    @api.depends('khs_ids.ips')
    def _compute_ipk(self):
        for nilai in self:
            val = {
                "total_tmp": 0,
                "total_sks_tmp": 0,
                "ipk": 0,
            }
        for rec in nilai.khs_ids:
            val["total_tmp"] += rec.total_tmp
            val["total_sks_tmp"] += rec.total_sks_tmp
            val["ipk"] = val["total_tmp"] / val["total_sks_tmp"]
        nilai.update(val)

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'
