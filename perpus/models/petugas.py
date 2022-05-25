from odoo import models, fields, api, _

class petugas(models.Model):
    # Attribute dari class Petugas
    _name = 'perpus.petugas'
    _description = 'Class Petugas Perpus UK Petra'

    # Attribute Fields
    id_petugas = fields.Char('ID', size=20, required=True, index=True, readonly=True,
                             states={'draft': [('readonly', False)]})
    name = fields.Char('Petugas', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    email = fields.Char('Email', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    no_telp = fields.Char('No Telepon', size=64, required=True, index=True, readonly=True,
                          states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # Constraint supaya unique id
    _sql_constraints = [('idpetugas_unik', 'unique(id_petugas)', _('ID Petugas must be unique!'))]

    # Def untuk di khs_views supaya statesnya dapat diupdate
    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'