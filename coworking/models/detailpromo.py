from datetime import datetime
from odoo import models, fields, api, _

class detailpromo(models.Model):
    _name = 'coworking.detaipromo'
    _description = 'Detail Promo CoWorking Spaces UK Petra'

    # Attribute Fields
    name = fields.Char('ID Detail Promo', size=64, required=True, index=True, readonly=True, default='new',
                       states={})
    redeem_code = fields.Boolean('Redeem Code', default=True, states={'draft': [('readonly', False)]})

    # Attribute ManytoOne refer to res_partner (member_id)
    member_id = fields.Many2one('res.partner', string='Member', readonly=True, ondelete="cascade", required=True,
                                states={'draft': [('readonly', False)]})

    # Attribute ManytoOne refer to res_partner (member_id)
    promo_id = fields.Many2one('coworking.promo', string='Kode Promo', readonly=False, ondelete="cascade",
                               states={'draft': [('readonly', False)]},
                               domain="[('state', '=', 'done')]")

    # Attribute related ke table lain
    point_minus = fields.Monetary("Current Point", compute='_compute_amount')
    min_amount = fields.Monetary("Minimum Amount", related='promo_id.min_amount')
    price_promo = fields.Monetary("Price Promo", related='promo_id.price_promo')

