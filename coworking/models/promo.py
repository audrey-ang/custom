from datetime import datetime
from odoo import models, fields, api, _

class promo(models.Model):
    _name = 'coworking.promo'
    _description = 'Promo CoWorking Spaces UK Petra'
    _rec_name = 'nama_promo'

    # Attribute Fields
    id_promo = fields.Char('ID Promo', size=64, required=True, index=True, readonly=False, default='new',
                           states={})
    nama_promo = fields.Char('Nama Promo', size=64, required=True, index=True, readonly=True,
                             states={'draft': [('readonly', False)]})
    jenis_promo = fields.Selection([('discount', 'Discount'),
                                    ('voucher', 'Voucher'),
                                    ('reimbursment', 'Reimbursment'),
                                    ('lainlain', 'Lainnya')], 'Jenis Promo', readonline=True, default='discount',
                                   states={'draft': [('readonly', False)]})
    date_start = fields.Datetime('Tanggal Event', readonly=True,
                                 states={'draft': [('readonly', False)]})
    date_end = fields.Datetime('Tanggal Event', readonly=True,
                               states={'draft': [('readonly', False)]})
    disc_percentage = fields.Float('Percentage Discount', store=True, default=0)
    min_pembelian = fields.Monetary(string="Minimum Amount", store=True)
    # max_diskon = fields.Monetary(string="Max Amount Discount", store=True)
    count_promo = fields.Integer('Initial Quantity', readonly=False, default=0)
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # Attribute OnetoMany refer to transaksi (transaksi_ids)
    transaksi_ids = fields.One2many('coworking.transaksi', 'promo_id', string='Transaksi')

    # Attribute ManytoOne refer to res_partner (member_id)
    member_id = fields.Many2one('res.partner', string='By', readonly=True, ondelete="cascade",
                                states={'draft': [('readonly', False)]})

    # Attribute related to currency
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env['res.company']._company_default_get(
                                     'account.budget.post'))
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True,
                                  related='company_id.currency_id')

    # Attribute related to table lain
    state_related = fields.Selection("State", related="transaksi_ids.state")

    #Attribute yang di Compute
    promo_count = fields.Integer("Used Promo", compute='_compute_jumlahpromo')
    sisa_promo = fields.Integer("Remaining Quantity", compute='_compute_sisapromo')

    # All Constraints
    _sql_constraints = [('check_min_pembelian', 'CHECK(min_pembelian >= 0)', "Minimum Amount can't minus"),
                        ('check_disc_percentage', 'CHECK(disc_percentage > 0)', "Discount Percentage must positive and can't be zero"),
                        ('check_count_promo', 'CHECK(count_promo >= 0)', "Count Promo can't minus")]

    def action_done(self):
        self.state = 'done'
        if self.id_promo == 'new' or not self.id_promo:
            seq = self.env['ir.sequence'].search([("code", "=", "coworking.promo.sequence")])
            if not seq:
                raise UserError(_("coworking.promo sequence not found, please create coworking.promo sequence"))
            self.id_promo = seq.next_by_code('coworking.promo.sequence')

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    def _compute_jumlahpromo(self):
        for rec in self:
            rec.promo_count = self.env['coworking.transaksi'].search_count([('promo_id', '=', rec.id), ('state', '=', 'done')])

    def promo_button(self):
        return{
            'name': 'Promo',
            'type': 'ir.actions.act_window',
            'res_model': 'coworking.transaksi',
            'view_mode': 'tree',
            'domain': [('promo_id', '=', self.id), ('state', '=', 'done')],
            'context': {'create': False}
        }

    @api.depends('transaksi_ids')
    def _compute_sisapromo(self):
        for coworking in self:
            sisa_promo = coworking.count_promo
            for rec in coworking.transaksi_ids:
                if rec.state == 'done':
                    sisa_promo -= 1
            coworking.update({
                'sisa_promo': sisa_promo,
            })
