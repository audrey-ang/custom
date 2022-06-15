{
    'name': 'Coworking',  # nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Audrey',
    'summary': 'Modul Coworking Spaces',  # deskripsi singkat dari modul
    'description': 'Ideas management module',  # bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    # di idea/static/description, bisa kasi icon modul juga.
    'category': 'Project UAS',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base', 'sale', 'product'],  # list of dependencies, conditioning startup order
    'data': [
        'security/ir.model.access.csv',
        'views/customer_views.xml',
        'views/ruangan_views.xml',
        'views/transaksi_views.xml',
        'views/event_views.xml',
        'views/promo_views.xml',
        'views/detailruangan_views.xml',
        'wizard/wiz_coworking_transaksi_views.xml',
        'data/ir_sequence_data.xml',
    ],
    'qweb': [],  # untuk memberi tahu static file, misal CSS
    'demo': [],  # demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}