from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'
    company_type = fields.Selection(selection_add=[('investor', 'Investor')], ondelete={'code': 'cascade'})

    #Attribute
    point = fields.Monetary(string="Point Member", compute='_compute_point')

    # Attribute OnetoMany refer to transaksi (transaksi_ids)
    transaksi_ids = fields.One2many('coworking.transaksi', 'member_id', string='Transaksi')

    @api.depends('transaksi_ids.state')
    def _compute_point(self):
        for coworking in self:
            point = 0
            for rec in coworking.transaksi_ids.filtered(lambda i: i.state == 'done'):
                point += rec.point_expected
            coworking.update({
                'point': point,
            })