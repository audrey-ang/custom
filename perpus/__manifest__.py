{
    'name': 'Perpustakaan',  # nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Audrey',
    'summary': 'Modul Peminjaman Perpustakaan UK Petra',  # deskripsi singkat dari modul
    'description': 'Ideas management module',
    'category': 'Latihan',
    'website': 'https://library.petra.ac.id',
    'depends': ['base', 'sales_team'],  # list of dependencies, conditioning startup order
    'data': [
        'views/anggota_views.xml',
        'views/buku_views.xml',
        'views/petugas_views.xml',
        'views/peminjaman_views.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml'
    ],
    'qweb': [],  # untuk memberi tahu static file, misal CSS
    'demo': [],  # demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}
