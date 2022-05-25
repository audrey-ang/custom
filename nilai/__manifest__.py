{
    'name': 'Nilai',  # nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Audrey',
    'summary': 'Modul KHS SIB UK Petra',  # deskripsi singkat dari modul
    'description': 'Ideas management module',  # bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    # di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base', 'sales_team'],  # list of dependencies, conditioning startup order
    'data': [
        'views/mahasiswa_views.xml',
        'views/matakuliah_views.xml',
        'views/khs_views.xml',
        'views/kelas_views.xml',
        'security/ir.model.access.csv',
        'wizard/wiz_nilai_kelas_views.xml',
    ],
    'qweb': [],  # untuk memberi tahu static file, misal CSS
    'demo': [],  # demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}