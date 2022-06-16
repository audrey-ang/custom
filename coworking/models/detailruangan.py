from datetime import datetime
from odoo import models, fields, api, _

class detailruangan(models.Model):
    _name = 'coworking.detailruangan'
    _description = 'Detail Ruangan CoWorking Spaces UK Petra'

    # Attribute Fields
    name = fields.Char('ID Detail Ruangan', size=64, required=True, index=True, readonly=True, default='new',
                       states={})
    harga_akhir = fields.Monetary(string="Harga Akhir", compute='_compute_last_price', store=True)
    date_start = fields.Datetime('Date Start', default=datetime.today(), readonly=True,
                                 states={'draft': [('readonly', False)]})
    date_end = fields.Datetime('Date End', default=datetime.today(), readonly=True,
                               states={'draft': [('readonly', False)]})
    unit = fields.Integer('Unit', store=True, default=1, readonly=True)

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # Attribute ManytoOne refer to Transaksi (transaksi_id)
    transaksi_id = fields.Many2one('coworking.transaksi', string='ID Transaksi', readonly=True, ondelete="cascade",
                                    states={'draft': [('readonly', False)]})

    # Attribute OnetoMany refer to Ruangan (ruangan_id)
    ruangan_id = fields.Many2one('coworking.ruangan', string='Nama Ruangan', readonly=True, ondelete="cascade",
                                    states={'draft': [('readonly', False)]},
                                    domain="[('state', '=', 'done')]")

    # Attribute ManytoOne refer to res_partner (member_id)
    member_id = fields.Many2one('res.partner', string='Organizer', readonly=True, ondelete="cascade",
                                states={'draft': [('readonly', False)]})

    # Attribute ManytoOne refer to Currency (currency_id)
    currency_id = fields.Many2one('res.currency', 'Currency', related='transaksi_id.currency_id')

    # Attribute related to table lain
    jenis_member = fields.Char("Tipe membership", related="transaksi_id.jenis_member")
    harga_awal = fields.Monetary(string="Harga Awal", related="ruangan_id.harga", readonly=False)
    state_transaksi = fields.Selection("State Transaksi", related="transaksi_id.state")

    # All Constraints
    _sql_constraints = [('check_harga_awal', 'CHECK (harga_awal >= 0)', "Harga awal can't minus"),
                        ('check_unit', 'CHECK(unit > 0)',('Unit must be greater than or equal to 1'))]

    # Fungsi Def supaya statesnya dapat diupdate
    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('harga_awal', 'unit')
    def _compute_last_price(self):
        for rec in self:
            val = {
                "harga_akhir": 0.0,
            }
            val["harga_akhir"] = (rec.harga_awal * rec.unit)
            rec.update(val)

