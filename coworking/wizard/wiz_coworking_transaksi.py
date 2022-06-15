from odoo import models, fields, api, _

class wiz_coworking_transaksi(models.TransientModel):
    _name = 'wiz.coworking.transaksi'
    _description = 'Class untuk menyimpan data coworking transaksi'

    # Related field
    transaksi_id = fields.Many2one('coworking.transaksi', string='ID Transaksi', readonly=True)
    member_id = fields.Many2one(related='transaksi_id.member_id')
    detailruangan_ids = fields.One2many('wiz.coworking.detailruangan', 'wiz_header_id', string='Ruangan')
    detailevent_ids = fields.One2many('wiz.coworking.detailevent', 'wiz_header_id', string='Event')

    @api.model
    def default_get(self,
                    fields_list):  # ini adalah common method, semacam constructor, akan dijalankan saat create object. Ini akan meng-overwrite default_get dari parent
        res = super(wiz_coworking_transaksi, self).default_get(fields_list)
        # res  merupakan dictionary beserta value yang akan diisi, yang sudah diproses di super class (untuk create record baru)
        res['transaksi_id'] = self.env.context['active_id']
        return res

    @api.onchange('transaksi_id')
    def onchange_transaksi_id(self):
        if not self.transaksi_id:
            return
        detailruangan_ids = self.env['wiz.coworking.detailruangan']
        detailevent_ids = self.env['wiz.coworking.detailevent']
        for rec in self.transaksi_id.detailruangan_ids:
            detailruangan_ids += self.env['wiz.coworking.detailruangan'].new({
                'wiz_header_id': self.id,
                'ruangan_id': rec.ruangan_id.id,
                'ref_detailruangan_id': rec.id
            })
        for rec in self.transaksi_id.detailevent_ids:
            detailevent_ids += self.env['wiz.coworking.detailevent'].new({
                'wiz_header_id': self.id,
                'event_id': rec.event_id.id,
                'ref_detailevent_id': rec.id
            })

    def action_confirm(self):
        for rec in self.detailruangan_ids:
            rec.ref_detailruangan_id.unit = rec.unit

class detail_ruangan_wiz(models.TransientModel):
    _name = 'wiz.coworking.detailruangan'
    _description = 'Class untuk menyimpan data nilai suatu detailruangan'

    wiz_header_id = fields.Many2one('wiz.coworking.transaksi', string='Detail Ruangan')
    ref_detailruangan_id = fields.Many2one('coworking.detailruangan')
    ruangan_id = fields.Many2one('coworking.ruangan', ondelete="restrict")
    unit = fields.Integer('Unit', readonly=False)
    slot_tersedia = fields.Integer('Quantity Ruangan', related='ruangan_id.sisa_ruangan')

class detail_event_wiz(models.TransientModel):
    _name = 'wiz.coworking.detailevent'
    _description = 'Class untuk menyimpan data nilai suatu detailevent'

    wiz_header_id = fields.Many2one('wiz.coworking.transaksi', string='Detail Event')
    ref_detailevent_id = fields.Many2one('coworking.detailevent')
    event_id = fields.Many2one('coworking.event', ondelete="restrict")
    harga_awal = fields.Monetary(string="Harga Awal", related='ref_detailevent_id.harga_awal')

    # Attribute related to currency
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env['res.company']._company_default_get(
                                     'account.budget.post'))
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True,
                                  related='company_id.currency_id')