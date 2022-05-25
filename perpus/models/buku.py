from odoo import models, fields, api, _
from odoo.exceptions import UserError

class buku(models.Model):
    # Attribute dari class Buku
    _name = 'perpus.buku'
    _description = 'Class Buku Perpus UK Petra'

    #Attribute Fields
    id_buku = fields.Char('ID', size=20, required=True, index=True, readonly=True, default='new',
                          states={})
    name = fields.Char('Judul Buku', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    pengarang = fields.Char('Pengarang', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    tahun = fields.Char('Tahun', size=20, default="2022", required=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    penerbit = fields.Char('Penerbit', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    harga = fields.Integer("Harga Pinjam", required=True, readonly=True, store=True,
                           states={'draft': [('readonly', False)]}, default=15000)
    harga_beli = fields.Integer("Harga Beli", required=True, readonly=True, store=True,
                                states={'draft': [('readonly', False)]}, default=15000)
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # Attribute OnetoMany refer to detail_peminjaman (detail_peminjaman_ids)
    detail_peminjaman_ids = fields.One2many('perpus.detailpeminjaman', 'buku_id', string='Detail Peminjaman')

    #Attribute yang di Compute
    stok = fields.Integer("Stok Buku", compute="_compute_stok", store=True, required=True, default=1,
                          states={'draft': [('readonly', False)]})

    #Attribute temporary
    stok_tmp = fields.Integer("Stok tmp")

    # Constraint check
    _sql_constraints = [('harga_check', 'CHECK (harga_beli > 0)', 'Harga harus diatas 0'),
                        ('stok_check', 'CHECK (stok >= 0)', 'Stok buku tidak boleh habis!')]

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
        seq = self.env['ir.sequence'].search([("code", "=", "perpus.buku")])
        if not seq:
            raise UserError(_("perpus.buku sequence not found, please create idea.idea sequence"))
        for val in vals_list:
            val['id_buku'] = seq.next_by_id(sequence_date=val['tahun'])

        return super(buku, self).create(vals_list)
        # nama class yg peminjaman ni

    # @api.depends('detail_peminjaman_ids')
    # def _compute_stok(self):
    #     for perpus in self:
    #         val = {
    #             "stok": self.stok + 1,
    #         }
    #         for rec in self:
    #             val["stok"] -= len(rec.id_buku) + 1
    #         perpus.update(val)
