import urllib.request
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from clinic.models import Procedure, ProcedureImage

PROCEDURES = [
    {
        'slug': 'neck-lift',
        'name_en': 'Neck Lift',
        'name_tr': 'Boyun Germe',
        'summary_en': 'Neck lift tightens loose skin and muscles in the neck and jawline for a smoother, more youthful profile.',
        'summary_tr': 'Boyun germe, boyun ve cene hattindaki gevsek deri ve kaslari sikilastirarak daha genc bir profil saglar.',
    },
    {
        'slug': 'double-chin-liposuction',
        'name_en': 'Double Chin Liposuction',
        'name_tr': 'Cene Alti Liposuction',
        'summary_en': 'Submental liposuction removes excess fat under the chin to define the jawline and reduce a double chin appearance.',
        'summary_tr': 'Cene alti liposuction, cene altindaki fazla yagi alarak cene hattini belirginlestirir.',
    },
    {
        'slug': 'eyebrow-transplant',
        'name_en': 'Eyebrow Transplant',
        'name_tr': 'Kas Ekimi',
        'summary_en': 'Eyebrow transplant restores natural, fuller brows using your own hair follicles for permanent results.',
        'summary_tr': 'Kas ekimi, kendi sac koklerinizle dogal ve kalici kaslar olusturur.',
    },
    {
        'slug': 'lip-filler',
        'name_en': 'Lip Filler',
        'name_tr': 'Dudak Dolgusu',
        'summary_en': 'Lip filler adds volume and shape to the lips with hyaluronic acid for natural, balanced enhancement.',
        'summary_tr': 'Dudak dolgusu, hyaluronik asit ile dudaklara hacim ve sekil kazandirir.',
    },
    {
        'slug': 'full-face-filler',
        'name_en': 'Full Face Filler',
        'name_tr': 'Tam Yuz Dolgusu',
        'summary_en': 'Full face filler restores volume, smooths wrinkles, and rejuvenates facial contours non-surgically.',
        'summary_tr': 'Tam yuz dolgusu, yuz konturunu ameliyatsiz sekilde genclendirir ve hacim kazandirir.',
    },
    {
        'slug': 'full-face-lift',
        'name_en': 'Full Face Lift',
        'name_tr': 'Tam Yuz Germe',
        'summary_en': 'Full face lift addresses sagging skin across the entire face for comprehensive rejuvenation.',
        'summary_tr': 'Tam yuz germe, yuzdeki sarkik deriyi kapsamli sekilde duzeltir.',
    },
    {
        'slug': 'midface-lift',
        'name_en': 'Midface Lift',
        'name_tr': 'Orta Yuz Germe',
        'summary_en': 'Midface lift elevates the cheeks and under-eye area to restore youthful midface volume.',
        'summary_tr': 'Orta yuz germe, yanaklari ve goz alti bolgesini kaldirarak genclik hacmi saglar.',
    },
    {
        'slug': 'upper-blepharoplasty',
        'name_en': 'Upper Blepharoplasty',
        'name_tr': 'Ust Blefaroplasti',
        'summary_en': 'Upper blepharoplasty removes excess upper eyelid skin for a refreshed, open-eyed appearance.',
        'summary_tr': 'Ust blefaroplasti, ust goz kapagi derisini alarak daha acik bir bakis saglar.',
    },
    {
        'slug': 'lower-blepharoplasty',
        'name_en': 'Lower Blepharoplasty',
        'name_tr': 'Alt Blefaroplasti',
        'summary_en': 'Lower blepharoplasty reduces under-eye bags and puffiness for a smoother lower eyelid.',
        'summary_tr': 'Alt blefaroplasti, goz alti torbalari ve siskinligi azaltir.',
    },
    {
        'slug': 'upper-lower-blepharoplasty',
        'name_en': 'Upper & Lower Blepharoplasty',
        'name_tr': 'Ust ve Alt Blefaroplasti',
        'summary_en': 'Combined upper and lower blepharoplasty rejuvenates the entire eye area in one procedure.',
        'summary_tr': 'Ust ve alt blefaroplasti birlikte tum goz cevresini genclendirir.',
    },
    {
        'slug': 'gynecomastia',
        'name_en': 'Gynecomastia',
        'name_tr': 'Jinekomasti',
        'summary_en': 'Gynecomastia surgery removes excess male breast tissue for a flatter, more masculine chest contour.',
        'summary_tr': 'Jinekomasti ameliyati, erkek gogus dokusunu alarak daha duz bir gogus hatti saglar.',
    },
    {
        'slug': 'abdominal-flank-lipomatic',
        'name_en': 'Abdominal & Flank Lipomatic',
        'name_tr': 'Karın ve Yan Lipomatik',
        'summary_en': 'Lipomatic removes stubborn fat from the abdomen and flanks for a slimmer, contoured waistline.',
        'summary_tr': 'Lipomatik, karın ve yan bolgelerdeki inatci yagi alarak bel hattini inceltir.',
    },
    {
        'slug': 'tummy-tuck',
        'name_en': 'Tummy Tuck',
        'name_tr': 'Karın Germe',
        'summary_en': 'Tummy tuck removes excess abdominal skin and tightens muscles for a firmer, flatter stomach.',
        'summary_tr': 'Karın germe, fazla karın derisini alir ve kaslari sikilastirir.',
    },
    {
        'slug': 'breast-lift',
        'name_en': 'Breast Lift',
        'name_tr': 'Meme Diklestirme',
        'summary_en': 'Breast lift raises and reshapes sagging breasts for a more youthful, elevated profile.',
        'summary_tr': 'Meme diklestirme, sarkik memeleri kaldirarak daha genc bir gorunum saglar.',
    },
    {
        'slug': 'breast-implants',
        'name_en': 'Breast Implants',
        'name_tr': 'Meme Protezi',
        'summary_en': 'Breast augmentation with implants increases volume and improves breast shape and symmetry.',
        'summary_tr': 'Meme protezi, hacim artisi ve daha simetrik bir meme formu saglar.',
    },
    {
        'slug': 'mammoplasty',
        'name_en': 'Mammoplasty',
        'name_tr': 'Mamoplasti',
        'summary_en': 'Mammoplasty reshapes the breasts through reduction, augmentation, or reconstruction based on your goals.',
        'summary_tr': 'Mamoplasti, hedeflerinize gore meme kucultme, buyutme veya rekonstruksiyon yapar.',
    },
    {
        'slug': 'otoplasty',
        'name_en': 'Otoplasty',
        'name_tr': 'Otoplasti',
        'summary_en': 'Otoplasty corrects prominent or misshapen ears for a more balanced facial appearance.',
        'summary_tr': 'Otoplasti, belirgin veya sekil bozuk kulaklari duzeltir.',
    },
    {
        'slug': 'hair-transplant',
        'name_en': 'Hair Transplant',
        'name_tr': 'Sac Ekimi',
        'summary_en': 'Hair transplant restores natural hair growth in thinning or balding areas using advanced FUE techniques.',
        'summary_tr': 'Sac ekimi, FUE teknikleriyle sac dokulmus bolgelerde dogal sac buyumesi saglar.',
    },
    {
        'slug': 'temple-lift',
        'name_en': 'Temple Lift',
        'name_tr': 'Sakak Germe',
        'summary_en': 'Temple lift elevates sagging skin at the temples and outer brow for a refreshed upper face.',
        'summary_tr': 'Sakak germe, sakak ve dis kas bolgesindeki sarkik deriyi kaldirarak ust yuzu genclendirir.',
    },
    {
        'slug': 'forehead-lift',
        'name_en': 'Forehead Lift',
        'name_tr': 'Alın Germe',
        'summary_en': 'Forehead lift smooths forehead wrinkles and raises the brows for a more alert, youthful look.',
        'summary_tr': 'Alın germe, alin kirisikliklarini duzeltir ve kaslari kaldirarak daha canli bir ifade saglar.',
    },
    {
        'slug': 'midface',
        'name_en': 'Midface',
        'name_tr': 'Orta Yuz',
        'summary_en': 'Midface procedures restore volume and lift to the central face, including cheeks and nasolabial folds.',
        'summary_tr': 'Orta yuz islemleri, yanaklar ve nazolabial cizgiler dahil merkezi yuze hacim ve lift saglar.',
    },
    {
        'slug': 'rhinoplasty',
        'name_en': 'Rhinoplasty',
        'name_tr': 'Rinoplasti',
        'summary_en': 'Rhinoplasty reshapes the nose to improve facial harmony, proportion, and breathing function.',
        'summary_tr': 'Rinoplasti, burnu yeniden sekillendirerek yuz uyumunu ve nefes fonksiyonunu iyilestirir.',
    },
]


def download_image(seed: str) -> bytes:
    url = f'https://picsum.photos/seed/{seed}/900/600'
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read()


class Command(BaseCommand):
    help = 'Replace all procedures with the clinic default procedure list.'

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        defaults_dir = media_root / 'procedures' / 'defaults'
        defaults_dir.mkdir(parents=True, exist_ok=True)

        deleted_images = ProcedureImage.objects.count()
        deleted_procedures = Procedure.objects.count()
        Procedure.objects.all().delete()

        self.stdout.write(
            self.style.WARNING(
                f'Deleted {deleted_procedures} procedures and {deleted_images} gallery items.'
            )
        )

        created = 0
        for item in PROCEDURES:
            image_bytes = download_image(item['slug'])
            procedure = Procedure(
                slug=item['slug'],
                name_en=item['name_en'],
                name_tr=item['name_tr'],
                summary_en=item['summary_en'],
                summary_tr=item['summary_tr'],
            )
            procedure.default_image.save(
                f"{item['slug']}.jpg",
                ContentFile(image_bytes),
                save=False,
            )
            procedure.save()
            created += 1
            self.stdout.write(f'  + {item["name_en"]}')

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created} procedures.'))
