from odoo import models, fields, api, _

class anggota(models.Model): #Inherit dari Model
    # Attribute dari class Anggota
    _name = 'perpus.anggota'
    _description = 'Class Anggota Perpus UK Petra'

    # Attribute Fields
    id_anggota = fields.Char('ID', size=20, required=True, index=True, readonly=True,
                    states={'draft': [('readonly', False)]})
    name = fields.Char('Anggota', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    # Res Partner untuk id_anggota
    # name = fields.Many2one('res.partner', 'Nama Anggota', readonly=True, default=lambda, states={'draft': [('readonly', False)]})
    email = fields.Char('Email', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    no_telp = fields.Char('No Telepon', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # Constraint supaya unique id
    _sql_constraints = [('idanggota_unik', 'unique(id_anggota)', _('ID Anggota must be unique!'))]

    # Def untuk di khs_views supaya statesnya dapat diupdate
    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'