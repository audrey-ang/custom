from odoo import models, fields, api, _
from odoo.exceptions import UserError

class idea(models.Model):  # inherit dari Model
    _name = 'idea.voting'  # attribute dari class Voting
    _description = 'class untuk berlatih ttg voting'
    _order = 'date desc'

    # Pembuatan attribute field
    name = fields.Char('Name', size=64, required=True, index=True, readonly=True, default='new',
                       states={})
    date = fields.Date('Date Voting', default=fields.Date.context_today, readonly=True, help='Please fill the date',
                       states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('voted', 'Voted'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')
    vote = fields.Selection([('yes', 'Yes'),
                             ('no', 'No'),
                             ('abstain', 'Abstain')], required=True,
                            readonly=True,
                            states={'draft': [('readonly', False)]})
    # many2one fields end with '_id' untuk fields voter
    voter_id = fields.Many2one('res.users', 'Voted By', readonly=True, ondelete="cascade", default=lambda self: self.env.user)
    # many2one fields idea_id
    idea_id = fields.Many2one('idea.idea', string='Idea', readonly=True, ondelete="cascade",
                              states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done'),('active', '=', 'True')]")

    #Related field ke table tertentu
    idea_date = fields.Date("Idea date", related='idea_id.date')

    def action_voted(self):
        self.state = 'voted'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env['ir.sequence'].search([("code", "=", "idea.voting")])
        if not seq:
            raise UserError(_("idea.voting sequence not found, please create idea.idea sequence"))
        for val in vals_list:
            val['name'] = seq.next_by_id(sequence_date=val['date'])

        return super(idea, self).create(vals_list)
        # nama class yg idea ni