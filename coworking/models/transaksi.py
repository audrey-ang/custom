from datetime import datetime
from odoo import models, fields, api, _

class transaksi(models.Model):
    _name = 'coworking.transaksi'
    _description = 'Transaksi CoWorking Spaces UK Petra'

    #Attribute Fields
    name = fields.Char('ID Transaksi', size=64, required=True, index=True, readonly=True, default='new',
                       states={})
    tgl_transaksi = fields.Date('Tanggal Transaksi', default=fields.Date.context_today, readonly=True, required=True,
                                states={'draft': [('readonly', False)]})
    status_pembayaran = fields.Selection([('paid', 'Lunas'),
                                          ('unpaid', 'Belum Lunas')],
                                          'Status Pembayaran', readonly=True, default='unpaid')
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # Attribute ManytoOne refer to res_partner (member_id)
    member_id = fields.Many2one('res.partner', string='Member', readonly=True, ondelete="cascade", required=True,
                                states={'draft': [('readonly', False)]})

    # Attribute ManytoOne refer to product.template (product_id) -> Alasannya karena membership dianggap product
    product_id = fields.Many2one('product.template', string='Membership', readonly=True, ondelete="cascade",
                                 states={'draft': [('readonly', False)]})

    # Attribute OnetoMany refer to detail_transaksi (detailruangan_ids)
    detailruangan_ids = fields.One2many('coworking.detailruangan', 'transaksi_id', string='Detail Ruangan')

    # Attribute OnetoMany refer to detail_transaksi (detailruangan_ids)
    detailevent_ids = fields.One2many('coworking.detailevent', 'transaksi_id', string='Detail Event')

    # Attribute ManytoOne refer to promo (promo_id)
    promo_id = fields.Many2one('coworking.promo', string='Kode Promo', readonly=True, ondelete="cascade",
                                 states={'draft': [('readonly', False)]},
                                 domain="[('state', '=', 'done')]")

    # Attribute related to table lain
    jenis_member = fields.Char("Tipe membership", related="category_id.name")
    category_id = fields.Many2one('product.category', string="test", related="product_id.categ_id")
    discount = fields.Float(string="Percentage Discount", related="promo_id.disc_percentage", store=True)
    min_amount = fields.Monetary(string="Minimum Amount", related="promo_id.min_pembelian")
    tgl_promo_start = fields.Date('Tanggal Promo Start', related="promo_id.date_start")
    tgl_promo_end = fields.Date('Tanggal Promo End', related="promo_id.date_end")
    sisa_promo = fields.Integer('Quantity Promo', related="promo_id.sisa_promo")
    max_discount = fields.Monetary('Max Discount', related="promo_id.max_discount")

    #Attribute yang di Compute
    biaya_total = fields.Monetary("Biaya Total", compute='_compute_amount', default=0)
    point_expected = fields.Monetary("Point Expected", compute='_compute_amount')

    # Attribute temporary
    selisih_1 = fields.Integer(string="Selisih", compute="_compute_selisih", store=True)
    selisih_2 = fields.Integer(string="Selisih", compute="_compute_selisih", store=True)

    # Attribute related to currency
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env['res.company']._company_default_get('account.budget.post'))
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True,
                                  related='company_id.currency_id')

    # All Constraint
    _sql_constraints = [('check_biaya_total', 'CHECK (biaya_total>=0)', "Total biaya can't minus"),
                        ('check_tgl_transaksi_start', 'CHECK(selisih_1 > 0)', 'Tgl transaksi must be between tgl_promo_start and tgl_promo_end'),
                        ('check_tgl_transaksi_end', 'CHECK(selisih_2 < 0)', 'Tgl transaksi must be between tgl_promo_start and tgl_promo_end'),]

    # Fungsi Def supaya statesnya dapat diupdate
    def action_done(self):
        self.state = 'done'
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "coworking.transaksi.sequence")])
            if not seq:
                raise UserError(_("coworking.transaksi sequence not found, please create coworking.transaksi sequence"))
            self.name = seq.next_by_code('coworking.transaksi.sequence')

        if self.status_pembayaran == 'unpaid':
            self.status_pembayaran = 'paid'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'
        if self.status_pembayaran == 'paid':
            self.status_pembayaran = 'unpaid'

    @api.depends('detailruangan_ids.harga_akhir', 'detailevent_ids.harga_akhir', 'promo_id.disc_percentage')
    def _compute_amount(self):
        for coworking in self:
            point_expected = biaya_total = 0
            for rec in coworking.detailruangan_ids:
                biaya_total += rec.harga_akhir
            for rec in coworking.detailevent_ids:
                biaya_total += rec.harga_akhir
            for rec in self:
                if biaya_total < rec.min_amount:
                    biaya_total = biaya_total
                else:
                    if(biaya_total * rec.discount < rec.max_discount):
                        biaya_total = biaya_total - (biaya_total * rec.discount)
                    else:
                        biaya_total = biaya_total - (rec.max_discount)
                if rec.jenis_member == "company" or rec.jenis_member == "Company":
                    point_expected = ((biaya_total / 100) * 1)
                elif rec.jenis_member == "personal" or rec.jenis_member == "Personal":
                    point_expected = ((biaya_total / 100) * 2)
                elif rec.jenis_member == "institution" or rec.jenis_member == "Institution":
                    point_expected = ((biaya_total / 100) * 3)
            coworking.update({
                'biaya_total': biaya_total,
                'point_expected': point_expected,
            })

    @api.depends('tgl_transaksi', 'tgl_promo_start', 'tgl_promo_end')
    def _compute_selisih(self):
        if self.tgl_promo_start and self.tgl_promo_end:
            for rec in self:
                selisih = int((rec.tgl_transaksi - rec.tgl_promo_start).days)
                selisih2 = int((rec.tgl_transaksi - rec.tgl_promo_end).days)
                rec.selisih_1 = selisih
                rec.selisih_2 = selisih2

    def action_wiz_transaksi(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard Detail Transaksi'),
            'res_model': 'wiz.coworking.transaksi',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

    def action_wiz_promo(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard Detail Promo'),
            'res_model': 'wiz.coworking.promo',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }
