{
    'name': 'Idea',  # nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Audrey',
    'summary': 'Modul Idea SIB UK Petra',  # deskripsi singkat dari modul
    'description': 'Ideas management module',  # bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    # di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base', 'sales_team'],  # list of dependencies, conditioning startup order
    'data': [
        'views/idea_views.xml',
        'views/voting_views.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml'
    ],
    'qweb': [],  # untuk memberi tahu static file, misal CSS
    'demo': [],  # demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}
