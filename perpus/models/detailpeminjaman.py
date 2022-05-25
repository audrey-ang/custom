from datetime import datetime
from odoo import models, fields, api, _

class detailpeminjaman(models.Model):
    # Attribute dari class Detail Peminjaman
    _name = 'perpus.detailpeminjaman'
    _description = 'Class Detail Peminjaman Perpus UK Petra'

    # Attribute Fields
    name = fields.Char(compute="_compute_name", store=True, recursive=True)
    tgl_kembali = fields.Date('Tanggal Pengembalian', readonly=True,
                             states={'draft': [('readonly', False)]})
    status_buku = fields.Selection([('hilang', 'Hilang'),
                                    ('cacat', 'Cacat'),
                                    ('rusak', 'Rusak'),
                                    ('aman', 'Aman')],
                                   'Status Buku', readonly=True, required=True, default='aman',
                                   states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # Attribute Fields Relationship

    # Attribute ManytoOne refer to Peminjaman (peminjaman_id)
    peminjaman_id = fields.Many2one('perpus.peminjaman', string='Nama Peminjam', readonly=True, ondelete="cascade",
                                    states={'draft': [('readonly', False)]},
                                    domain="[('state', '=', 'done')]")

    # Attribute ManytoOne refer to Buku (buku_id)
    buku_id = fields.Many2one('perpus.buku', string='Judul Buku', readonly=True, ondelete="cascade",
                              states={'draft': [('readonly', False)]},
                              domain="[('state', '=', 'done')]")

    #Attribute yang di Compute
    biaya_peminjaman = fields.Integer("Biaya Pinjam", compute="_compute_pinjam", store=True, default=0)
    biaya_denda = fields.Integer("Biaya Denda", compute="_compute_denda", store=True, default=0)
    biaya_terlambat = fields.Integer("Biaya Terlambat", compute="_compute_denda", store=True, default=0)

    # Attribute related ke Class lain
    tgl_peminjaman = fields.Date("Tanggal Pinjam", related='peminjaman_id.tgl_pinjam')
    harga_buku = fields.Integer("Harga Pinjam", related='buku_id.harga')
    harga_beli_buku = fields.Integer("Harga Beli", related='buku_id.harga_beli')

    # Attribute temporary
    selisih = fields.Integer(string="Selisih", compute="_compute_selisih", store=True)

    # Constraint supaya unique namenya
    _sql_constraints = [('selisih_check', 'CHECK(selisih >= 1)', _('Tanggal Kembalian harus lebih besar dibanding Tanggal Pinjam')),
                        ('terlambat_check', 'CHECK(biaya_terlambat >= 0)', _('Biaya keterlambatan tidak boleh minus'))
                        ]

    # Def untuk di khs_views supaya statesnya dapat diupdate
    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    # Context dari idea
    def tes_bookrent(self):
        print("ini di detailpeminjaman")
        #Opsi 1
        t = self.env.context.get('keterangan')
        print(t)

        # #Opsi 2
        # t = self.env.context
        # print(t.keterangan)

    @api.depends('tgl_peminjaman', 'tgl_kembali')
    def _compute_selisih(self):
        if self.tgl_peminjaman and self.tgl_kembali:
            for rec in self:
                selisih = int((rec.tgl_kembali - rec.tgl_peminjaman).days) + 1
                rec.selisih = selisih

    @api.depends('selisih', 'harga_buku')
    def _compute_pinjam(self):
        for perpus in self:
            val = {
                "biaya_peminjaman": 0
            }
            val["biaya_peminjaman"] += self.selisih * self.harga_buku
        perpus.update(val)

    @api.depends('status_buku', 'harga_beli_buku')
    def _compute_denda(self):
        for perpus in self:
            val = {
                "biaya_denda": 0
            }
            for rec in self:
                if self.status_buku == "hilang":
                    val["biaya_denda"] = (1.25 * rec.harga_beli_buku)
                elif self.status_buku == "cacat":
                    val["biaya_denda"] = (0.25 * rec.harga_beli_buku)
                elif self.status_buku == "rusak":
                    val["biaya_denda"] = (0.5 * rec.harga_beli_buku)
                else:
                    val["biaya_denda"] = 0
            perpus.update(val)






