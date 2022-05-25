# Tiap kali buat .py baru, attribute fields _name wajib ada. Alasannya karena itu inisialisasi model yg ada
# Tiap kali buat .py baru, attribute fields state wajib ada. Alasannya karena itu dibutuhin untuk set Relationship attribute + View di XML

# CTRL + / -> Buat commend
# Format ManytoOne -> Fieldsnya dinamakan partner_id, res.partner -> Relasi ke .py yg mana cth (nilai.mahasiswa)
# partner_id = fields.Many2one("res.partner", string="Partner")

# Format OnetoMany -> Wajib ditambahin s diakhir -> partner_id ambil dari relasi ManytoOne diatas
# test_ids = fields.One2many("test.model", "partner_id", string="Tests")

# total_yes = fields.Integer("Yes", compute="_compute_vote", store=True, default=0)
# total_no = fields.Integer("No", compute="_compute_vote", store=True, default=0)
# total_abstain = fields.Integer("Abstain", compute="_compute_vote", store=True, default=0)

# for nilai in self:
#     val = {
        # # Di dalam sini harus mengambil attribute yang sudah dideklarasikan yang diatasnya
        # "total_yes": 0,
        # "total_no": 0,
        # "total_abstain": 0
    # }
