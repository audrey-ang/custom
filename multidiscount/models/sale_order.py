from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    total_disc = fields.Monetary(string="Total Disc 1", compute='_amount_all', store=True)
    total_disc2 = fields.Monetary(string="Total Disc 2", compute='_amount_all', store=True)

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = total_disc = total_disc2 = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                subtotal = line.price_unit * line.product_uom_qty
                total_disc += line.discount/100 * subtotal
                total_disc2 += (subtotal-total_disc) * line.disc2/100
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
                'total_disc': total_disc,
                'total_disc2': total_disc2,
            })

class SaleOrderLines(models.Model):
    _inherit = 'sale.order.line'

    #Attribute
    disc2 = fields.Float(string="Disc 2 (%)", digits='Discount', default=0.0)

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'disc2')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            price = price * (1 - (line.disc2 or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups(
                    'account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])

