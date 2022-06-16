from datetime import datetime
from odoo import models, fields, api, _

class event(models.Model):
    _name = 'coworking.event'
    _description = 'Event CoWorking Spaces UK Petra'
    _rec_name = 'nama_event'

    #Attribute Fields
    name = fields.Char('ID Event', size=64, required=True, index=True, readonly=True, default='new',
                       states={})
    nama_event = fields.Char('Nama Event', size=64, required=True, index=True, readonly=True,
                             states={'draft': [('readonly', False)]})
    jenis_event = fields.Selection([('seminar', 'Seminar'),
                                    ('workshop', 'Workshop'),
                                    ('miniclass', 'Mini Class'),
                                    ('competition', 'Competition'),
                                    ('lainlain', 'Lainnya')], 'Jenis Event', readonline=True, default='Lainnya',
                                   required=True, states={'draft': [('readonly', False)]})
    date_start = fields.Datetime('Tanggal Event', default=datetime.today(), readonly=True, required=True,
                                 states={'draft': [('readonly', False)]})
    date_end = fields.Datetime('Tanggal Event', default=datetime.today(), readonly=True, required=True,
                               states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # Attribute ManytoOne refer to res_partner (member_id)
    category_id = fields.Many2one('product.category', string='Jenis Member', readonly=True, ondelete="cascade",
                                  states={'draft': [('readonly', False)]})

    # Attribute ManytoOne refer to res_partner (member_id)
    member_id = fields.Many2one('res.partner', string='Organizer', readonly=True, ondelete="cascade",
                                states={'draft': [('readonly', False)]})

    # Attribute related to table lain
    jenis_member = fields.Char("Tipe membership", related="category_id.name")

    # Fungsi Def supaya statesnya dapat diupdate
    def action_done(self):
        self.state = 'done'
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "coworking.event.sequence")])
            if not seq:
                raise UserError(_("coworking.event sequence not found, please create coworking.event sequence"))
            self.name = seq.next_by_code('coworking.event.sequence')

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'