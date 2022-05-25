from odoo import models, fields, api, _

class nilai(models.Model):  # inherit dari Model
    # Attribute dari class Mata Kuliah
    _name = 'nilai.matakuliah'
    _description = 'Class Mata Kuliah SIB UK Petra'

    # Secara default akan ditambahkan setelah Mata Kuliah / namaMK
    name = fields.Char('Nama Mata Kuliah', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    
    # Attribute Fields
    kodeMK = fields.Char('Kode Mata Kuliah', size=64, required=True, index=True, readonly=True,
                            states={'draft': [('readonly', False)]})

    sks = fields.Integer('SKS', default='3', required=True, readonly=False)
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # Constraint supaya unique namenya
    _sql_constraints = [('name_unik', 'unique(name)', _('Ideas must be unique!'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'