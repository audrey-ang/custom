from datetime import datetime
from odoo import models, fields, api, _

class ruangan(models.Model):
    _name = 'coworking.ruangan'
    _description = 'Ruangan CoWorking Spaces UK Petra'
    _rec_name = 'nama_ruangan'

    #Attribute Fields
    name = fields.Char('ID Ruangan', size=64, required=True, index=True, readonly=False, default='new',
                       states={})
    nama_ruangan = fields.Char('Nama Ruangan', size=64, required=True, index=True, readonly=True,
                             states={'draft': [('readonly', False)]})
    status_ruangan = fields.Boolean('Status Tersedia', default=True, states={'draft': [('readonly', False)]})
    kapasitas = fields.Integer("Kapasitas", required=True, readonly=True, store=True,
                               states={'draft': [('readonly', False)]}, default=1)
    jam_kerja_start = fields.Char("Jam kerja start", default='08.00')
    jam_kerja_end = fields.Char("Jam kerja end", default='17.00')
    fasilitas = fields.Text("Deskripsi Ruangan")
    harga = fields.Monetary(string="Harga sewa ruangan", store=True, required=True)
    slot_tersedia = fields.Integer("Initial Ruangan", default='1',
                                   states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # Attribute OnetoMany refer to detail_transaksi (detailruangan_ids)
    detailruangan_ids = fields.One2many('coworking.detailruangan', 'ruangan_id', string='Detail Ruangan')

    # Attribute related to currency
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env['res.company']._company_default_get('account.budget.post'))
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True,
                                  related='company_id.currency_id')

    #Attribute yang di Compute
    sisa_ruangan = fields.Integer("Quantity Ruangan", compute='_compute_sisaruangan')
    ruangan_count = fields.Integer("Used Ruangan", compute="_compute_jumlahruangan")

    # All Constraints
    _sql_constraints = [('check_harga', 'CHECK(harga >= 0)', "Harga can't minus"),
                        ('check_kapasitas', 'CHECK(kapasitas > 0)', "Kapasitas must be greater than or equal to 1"),
                        ('check_slot_tersedia', 'CHECK(slot_tersedia >= 0)', "Initial Ruangan can't minus")]

    # Fungsi Def supaya statesnya dapat diupdate
    def action_done(self):
        self.state = 'done'
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "coworking.ruangan.sequence")])
            if not seq:
                raise UserError(_("coworking.ruangan sequence not found, please create coworking.ruangan sequence"))
            self.name = seq.next_by_code('coworking.ruangan.sequence')

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('detailruangan_ids')
    def _compute_sisaruangan(self):
        for coworking in self:
            sisa_ruangan = coworking.slot_tersedia
            for rec in coworking.detailruangan_ids:
                if rec.state_transaksi == 'done':
                    sisa_ruangan -= 1
            coworking.update({
                'sisa_ruangan': sisa_ruangan,
            })

    def _compute_jumlahruangan(self):
        for rec in self:
            rec.ruangan_count = self.env['coworking.detailruangan'].search_count([('ruangan_id', '=', rec.id), ('state_transaksi', '=', 'done')])

    def ruangan_button(self):
        return{
            'name': 'Ruangan',
            'type': 'ir.actions.act_window',
            'res_model': 'coworking.detailruangan',
            'view_mode': 'tree',
            'domain': [('ruangan_id', '=', self.id), ('state_transaksi', '=', 'done')],
            'context': {'create': False}
        }