from odoo import models, fields, api, _
from odoo.exceptions import UserError

class idea(models.Model):  # inherit dari Model
    _name = 'idea.idea'  # atribut dari class Model
    _description = 'class untuk berlatih ttg idea'
    # rec_name = 'name'
    _order = 'date desc'  # defaultnya adalah id, pengaruhnya saat list view
    # id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # membuat attribute field
    name = fields.Char('Number', size=64, required=True, index=True, readonly=True, default='new',
                       states={})

    date = fields.Date('Date Release', default=fields.Date.context_today, readonly=True,
                       states={'draft': [('readonly', False)]})

    state = fields.Selection(
        [('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
         ('confirmed', 'Confirmed'),
         ('done', 'Done'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')  # tuple / record di dalam list, nama field harus state spy bisa diakses oleh states
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})
    confirm_date = fields.Date('Confirm date')

    confirm_partner_id = fields.Many2one('res.partner', 'Confirm By', readonly=True)
    # Ketambahan voting_ids supaya bs ambil dari votings.py, s -> ditambahin karena penamaan default di odoo 1:M
    voting_ids = fields.One2many('idea.voting', 'idea_id', string='Votes')
    total_yes = fields.Integer("Yes", compute="_compute_vote", store=True, default=0)
    total_no = fields.Integer("No", compute="_compute_vote", store=True, default=0)
    total_abstain = fields.Integer("Abstain", compute="_compute_vote", store=True, default=0)

    score = fields.Integer('Score', default=0, readonly=True)
    # sponsor_ids = fields.Many2many('res.partner', 'idea_idea_res_partner_rel', 'idea_idea_id', 'res_partner_id', 'Sponsors')
    sponsor_ids = fields.Many2many('res.partner', string='Sponsors')
    owner = fields.Many2one('res.partner', 'Owner', index=True, readonly=True, states={'draft': [('readonly', False)]})
    _sql_constraints = [('name_unik', 'unique(name)', _('Ideas must be unique!'))]

    @api.depends("voting_ids", "voting_ids.vote", "voting_ids.state")
    # function api ini dijalankan:
    # 1. Tiap kali ada new record refer to voting_ids
    # 2. Tiap kali ada radio button vote pada voting.py berubah (yes, no, abstain)
    # 3. Tiap kali state pada voting.py berubah (canceled, settodraft, confirmed)

    def _compute_vote(self):
        for idea in self.filtered(
                lambda s: s.state == "done"):  # State 'Done' di idea untuk bisa di voting. Selain done ga bs di voting
            val = {
                "total_yes": 0,
                "total_no": 0,
                "total_abstain": 0
            }
            for rec in idea.voting_ids.filtered(
                    lambda s: s.state == "voted"):  # State 'voted' di voting untuk bisa di + jumlah votenya
                # State 'canceled, draft' tidak akan di count +nya
                # lambda merupakan on the fly function dari phyton
                # s ini adalah self dari voting_ids, fungsi filtered ini akan memfilter khusus state yang bernilai voted
                # bisa pake looping, ga ush difilter. Tapi pengecekan tidak efisien
                # karena misal ada 100 data, trs hanya 2 yang canceled berarti tetep 100 pengecekan. Sedangkan filter hanya 2x saja
                if rec.vote == "yes":
                    val["total_yes"] += 1
                elif rec.vote == "no":
                    val["total_no"] += 1
                else:
                    val["total_abstain"] += 1

            idea.update(val)

    def action_done(self):
        self.state = 'done'
        t = self.env.context
        print(t.get('keterangan'))

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "idea.idea")])
            if not seq:
                raise UserError(_("idea.idea sequence not found, please create idea.idea sequence"))
            self.name = seq.next_by_id(sequence_date=self.date)

    def action_settodraft(self):
        self.state = 'draft'

    def action_tes(self):
        # Pencet F8 buat debug yg biru2 di run
        # Contoh ambil dari active user
        print(self.env.user.name)
        # Contoh ambil active company
        print(self.env.company.name)
        # Contoh common ORM method search
        a = self.env["res.partner"].search([('name', 'ilike', 'Gemini')])
        for rec in a:
            print(rec.name)
        a = self.env["res.partner"].search([], limit=2)

        # Context
        print(self.env.context.get('lang'))

        #Memanggil function di model yang sama dengan memassingkan context
        t = self.env.context.copy()
        t["keterangan"] = 'Ideku'
        self.with_context(t).action_done()

        #Passing value dari object lain
        b = self.env['perpus.detailpeminjaman']  # b adalah object dari model perpus.detailpeminjaman
        b.with_context(t).tes_bookrent()  # memanggil function di object dari model lain dengan memassingkan context

        # Cursor

        #Contoh query select
        query = "SELECT name FROM res_partner ORDER BY name DESC LIMIT 3"
        self.env.cr.execute(query)
        res = self.env.cr.fetchall()
        for data in res:
            print(data[0])

        #Contoh query update
        query = "UPDATE idea_idea SET states='done' WHERE state IN ('confirmed', 'draft')"
        self.env.cr.execute(query)
        self.env.cr.rollback()

        #Contoh query delete
        query = "DELETE FROM idea_idea WHERE status='draft'"
        self.env.cr.execute(query)
        self.env.cr.rollback()

        # Contoh browse
        query = "SELECT * FROM res_partner LIMIT 3"
        self.env.cr.execute(query)
        res = self.env["res.partner"].browse(ro)
