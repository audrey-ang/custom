from odoo import models, fields, api, _
from odoo.exceptions import UserError

class peminjaman(models.Model):
    # Attribute dari class Peminjaman
    _name = 'perpus.peminjaman'
    _description = 'Class Peminjaman Perpus UK Petra'

    # Attribute Fields
    name = fields.Char('ID', size=20, required=True, index=True, readonly=True, default='new',
                       states={})
    tgl_pinjam = fields.Date('Tanggal Peminjaman', default=fields.Date.context_today, readonly=True,
                             states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # Attribute Fields Relationship

    # Attribute OnetoMany refer to detail_peminjaman (detail_peminjaman_ids)
    detail_peminjaman_ids = fields.One2many('perpus.detailpeminjaman', 'peminjaman_id', string='Detail Peminjaman')

    # Attribute ManytoOne refer to Petugas (petugas_id)
    petugas_id = fields.Many2one('perpus.petugas', string='Petugas', readonly=True, ondelete="cascade",
                                 states={'draft': [('readonly', False)]},
                                 domain="[('state', '=', 'done')]")

    # Attribute ManytoOne refer to Anggota (anggota_id)
    anggota_id = fields.Many2one('perpus.anggota', string='Anggota', readonly=True, ondelete="cascade",
                                 states={'draft': [('readonly', False)]},
                                 domain="[('state', '=', 'done')]")

    #Attribute yang di Compute
    total_peminjaman = fields.Integer("Quantity", compute="_compute_jumlahpinjam", store=True, default=0)
    biaya_total = fields.Integer("Biaya Total", compute="_compute_total", store=True, default=0)

    # Attribute related to table lain
    biaya_peminjaman = fields.Integer("Harga Pinjam", related='detail_peminjaman_ids.biaya_peminjaman')
    biaya_denda = fields.Integer("Harga Denda", related='detail_peminjaman_ids.biaya_denda')

    # Constraint supaya unique namenya
    _sql_constraints = [('peminjaman_unik', 'unique(id)', _('ID Peminjaman must be unique!')),
                        ('denda_check', 'CHECK(biaya_denda) >= 0', _('Biaya denda tidak boleh minus')),
                        ('total_check', 'CHECK(biaya_total) >= 0', _('Biaya total tidak boleh minus')),
                        ('total_peminjaman_check', 'CHECK(total_peminjaman) >= 0 AND CHECK(total_peminjaman) <= 3)', _('Batas peminjaman hanya boleh maks 3!'))
                        ]

    # Def untuk di khs_views supaya statesnya dapat diupdate
    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    # Untuk save lalu di generate name secara sequence
    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env['ir.sequence'].search([("code", "=", "perpus.peminjaman")])
        if not seq:
            raise UserError(_("idea.voting sequence not found, please create idea.idea sequence"))
        for val in vals_list:
            val['name'] = seq.next_by_id(sequence_date=val['tgl_pinjam'])

        return super(peminjaman, self).create(vals_list)
        # nama class yg peminjaman ni

    @api.depends('detail_peminjaman_ids.biaya_peminjaman', 'detail_peminjaman_ids.biaya_denda')
    def _compute_total(self):
        for perpus in self:
            val = {
                "biaya_total": 0
            }
            for rec in perpus.detail_peminjaman_ids:
                val["biaya_total"] += rec.biaya_peminjaman
                val["biaya_total"] += rec.biaya_denda
            perpus.update(val)

    @api.depends('detail_peminjaman_ids')
    def _compute_jumlahpinjam(self):
        for perpus in self:
            val = {
                "total_peminjaman": 0
            }
            for rec in perpus.detail_peminjaman_ids:
                val["total_peminjaman"] += len(rec.buku_id)
            perpus.update(val)

    # @api.depends('detail_peminjaman_ids')
    # def _compute_jumlahpinjam(self):
    #     for perpus in self:
    #         val = {
    #             "total_peminjaman": 0
    #         }
    #         val["total_peminjaman"] += len(buku_id)
    #     perpus.update(val)