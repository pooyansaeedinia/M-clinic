UI_TEXTS = {
    'en': {
        'brand_subtitle': 'Plastic Surgery',
        'home': 'Home',
        'login': 'Login',
        'logout': 'Logout',
        'add_procedure': 'Add Procedure',
        'manage_content': 'Manage Content',
        'add_images': 'Add New Before & After',
        'edit_procedure': 'Edit Procedure',
        'delete_procedure': 'Delete Procedure',
        'edit_image': 'Edit Image',
        'delete_image': 'Delete Image',
        'procedures': 'Popular Procedures',
        'view_details': 'View Details',
        'before_after': 'Before & After Samples',
        'before': 'Before',
        'after': 'After',
        'about_procedure': 'About Procedure',
        'no_samples': 'No before/after images yet.',
        'save': 'Save',
        'update': 'Update',
        'cancel': 'Cancel',
        'confirm_delete': 'Are you sure?',
        'content_dashboard': 'Content Dashboard',
        'gallery_count': 'Gallery Items',
        'pick_language': 'Language',
    },
    'tr': {
        'brand_subtitle': 'Plastik Cerrahi',
        'home': 'Ana Sayfa',
        'login': 'Giris',
        'logout': 'Cikis',
        'add_procedure': 'Yeni Islem Ekle',
        'manage_content': 'Icerik Yonetimi',
        'add_images': 'Yeni Once & Sonra Ekle',
        'edit_procedure': 'Islemi Duzenle',
        'delete_procedure': 'Islemi Sil',
        'edit_image': 'Gorseli Duzenle',
        'delete_image': 'Gorseli Sil',
        'procedures': 'Populer Islemler',
        'view_details': 'Detaylari Gor',
        'before_after': 'Once & Sonra Ornekleri',
        'before': 'Once',
        'after': 'Sonra',
        'about_procedure': 'Islem Hakkinda',
        'no_samples': 'Henuz once/sonra gorseli yok.',
        'save': 'Kaydet',
        'update': 'Guncelle',
        'cancel': 'Iptal',
        'confirm_delete': 'Emin misiniz?',
        'content_dashboard': 'Icerik Paneli',
        'gallery_count': 'Galeri Kayitlari',
        'pick_language': 'Dil',
    },
}


def global_context(request):
    current_lang = request.session.get('lang', 'en')
    if current_lang not in UI_TEXTS:
        current_lang = 'en'

    return {
        'current_lang': current_lang,
        'texts': UI_TEXTS[current_lang],
    }
