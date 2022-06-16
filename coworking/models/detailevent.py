from datetime import datetime
from odoo import models, fields, api, _

class detailevent(models.Model):
    _name = 'coworking.detailevent'
    _description = 'Detail Event CoWorking Spaces UK Petra'

    # Attribute Fields
    name = fields.Char('ID Detail Event', size=64, required=True, index=True, readonly=True, default='new',
                       states={})
    harga_awal = fields.Monetary(string="Harga Awal", store=True, required=True)
    harga_akhir = fields.Monetary(string="Harga Akhir", compute='_compute_last_price', store=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # Attribute ManytoOne refer to Transaksi (transaksi_id)
    transaksi_id = fields.Many2one('coworking.transaksi', string='ID Transaksi', readonly=True, ondelete="cascade",
                                    states={'draft': [('readonly', False)]})

    # Attribute OnetoMany refer to Ruangan (ruangan_id)
    event_id = fields.Many2one('coworking.event', string='Nama Event', readonly=True, ondelete="cascade",
                                 states={'draft': [('readonly', False)]},
                                 domain="[('state', '=', 'done')]")

    # Attribute ManytoOne refer to res_partner (member_id)
    member_id = fields.Many2one('res.partner', string='Organizer', readonly=True, ondelete="cascade",
                                states={'draft': [('readonly', False)]})

    # Attribute ManytoOne refer to Currency (currency_id)
    currency_id = fields.Many2one('res.currency', 'Currency', related='transaksi_id.currency_id')

    # Attribute related to table lain
    jenis_member = fields.Char("Tipe membership", related="transaksi_id.jenis_member")
    date_start = fields.Datetime('Date Start', related="event_id.date_start", readonly=True)
    date_end = fields.Datetime('Date End', related="event_id.date_end", readonly=True)

    # Attribute temporary
    selisih = fields.Integer(string="Selisih", compute="_compute_selisih", store=True)

    # All Constraints
    _sql_constraints = [('check_harga_awal', 'CHECK(harga_awal >= 0)', "Harga awal can't minus"),
                        ('check_harga_akhir', 'CHECK(harga_akhir > 0)', "Harga akhir can't minus")]

    # Fungsi Def supaya statesnya dapat diupdate
    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('harga_awal', 'selisih')
    def _compute_last_price(self):
        # for coworking in self:
        for rec in self:
            val = {
                "harga_akhir": 0.0,
                "harga_akhir_event": 0.0
            }
            val["harga_akhir"] = (rec.harga_awal * rec.selisih)
            val["harga_akhir_event"] += (rec.harga_awal * rec.selisih)
            rec.update(val)

    @api.depends('date_start', 'date_end')
    def _compute_selisih(self):
        if self.date_start and self.date_end:
            for rec in self:
                selisih = int((rec.date_start - rec.date_end).days) + 1
                rec.selisih = selisih