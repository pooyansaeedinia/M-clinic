from functools import wraps
from pathlib import Path

from django.conf import settings
from django.db.models import Case, Count, IntegerField, Value, When
from django.shortcuts import redirect
from django.urls import reverse

PORTAL_SESSION_KEY = 'portal_authenticated'
PORTAL_USERNAME = 'pooyan'
PORTAL_PASSWORD = '1234'

ENGLISH_CODE = 'english'

# Display order and names for the dashboard language cards.
DEFAULT_LANGUAGES = [
    {
        'code': 'english',
        'name': 'English',
        'language_name': 'English',
        'sort_order': 0,
        'legacy_codes': ('en', 'united-kingdom'),
        'flag_colors': ('#012169', '#C8102E', '#FFFFFF'),
    },
    {
        'code': 'turkiye',
        'name': 'Türkiye',
        'language_name': 'Turkish',
        'sort_order': 1,
        'legacy_codes': ('tr',),
        'flag_colors': ('#E30A17', '#FFFFFF'),
    },
    {
        'code': 'germany',
        'name': 'Germany',
        'language_name': 'German',
        'sort_order': 2,
        'legacy_codes': ('de',),
        'flag_colors': ('#000000', '#DD0000', '#FFCE00'),
    },
    {
        'code': 'spain',
        'name': 'Spain',
        'language_name': 'Spanish',
        'sort_order': 3,
        'legacy_codes': ('es',),
        'flag_colors': ('#AA151B', '#F1BF00'),
    },
    {
        'code': 'arabic',
        'name': 'Arabic',
        'language_name': 'Arabic',
        'sort_order': 4,
        'legacy_codes': ('ar', 'saudi-arabia'),
        'flag_colors': ('#165d31', '#FFFFFF'),
    },
    {
        'code': 'france',
        'name': 'France',
        'language_name': 'French',
        'sort_order': 5,
        'legacy_codes': ('fr',),
        'flag_colors': ('#002395', '#FFFFFF', '#ED2939'),
    },
    {
        'code': 'russia',
        'name': 'Russia',
        'language_name': 'Russian',
        'sort_order': 6,
        'legacy_codes': ('ru',),
        'flag_colors': ('#FFFFFF', '#0039A6', '#D52B1E'),
    },
]


def is_portal_authenticated(request):
    return request.session.get(PORTAL_SESSION_KEY) is True


def portal_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_portal_authenticated(request):
            return redirect(reverse('portal_login'))
        return view_func(request, *args, **kwargs)

    return wrapper


def languages_queryset():
    """Languages with English pinned first, then sort_order / name."""
    from .models import ChatTemplateLanguage

    return ChatTemplateLanguage.objects.annotate(
        english_first=Case(
            When(code=ENGLISH_CODE, then=Value(0)),
            When(name__iexact='English', then=Value(0)),
            default=Value(1),
            output_field=IntegerField(),
        ),
        section_count=Count('sections'),
    ).order_by('english_first', 'sort_order', 'name')


def _write_default_flag_png(code, colors):
    from PIL import Image, ImageDraw

    directory = Path(settings.BASE_DIR) / 'static' / 'portal' / 'languages'
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f'{code}.png'
    if path.exists():
        return path

    width, height = 480, 320
    image = Image.new('RGB', (width, height), colors[0])
    draw = ImageDraw.Draw(image)

    if code == 'english':
        draw.rectangle([0, 0, width, height], fill='#012169')
        draw.line([(0, 0), (width, height)], fill='#FFFFFF', width=48)
        draw.line([(width, 0), (0, height)], fill='#FFFFFF', width=48)
        draw.line([(0, 0), (width, height)], fill='#C8102E', width=24)
        draw.line([(width, 0), (0, height)], fill='#C8102E', width=24)
        draw.rectangle([width // 2 - 40, 0, width // 2 + 40, height], fill='#FFFFFF')
        draw.rectangle([0, height // 2 - 40, width, height // 2 + 40], fill='#FFFFFF')
        draw.rectangle([width // 2 - 24, 0, width // 2 + 24, height], fill='#C8102E')
        draw.rectangle([0, height // 2 - 24, width, height // 2 + 24], fill='#C8102E')
    elif code == 'turkiye':
        draw.ellipse([110, 80, 250, 240], fill='#FFFFFF')
        draw.ellipse([145, 95, 265, 225], fill='#E30A17')
        draw.polygon(
            [(300, 160), (325, 168), (318, 142), (340, 126), (312, 126), (300, 100),
             (288, 126), (260, 126), (282, 142), (275, 168)],
            fill='#FFFFFF',
        )
    elif code in {'germany', 'russia'}:
        band = height // 3
        draw.rectangle([0, 0, width, band], fill=colors[0])
        draw.rectangle([0, band, width, band * 2], fill=colors[1])
        draw.rectangle([0, band * 2, width, height], fill=colors[2])
    elif code == 'spain':
        draw.rectangle([0, 0, width, height], fill=colors[0])
        draw.rectangle([0, height // 4, width, (height * 3) // 4], fill=colors[1])
    elif code == 'arabic':
        draw.rectangle([0, 0, width, height], fill=colors[0])
        draw.rectangle([90, 120, 390, 140], fill='#FFFFFF')
        draw.rectangle([110, 155, 370, 170], fill='#FFFFFF')
        draw.polygon([(90, 210), (390, 210), (405, 235), (75, 235)], fill='#FFFFFF')
    elif code == 'france':
        band = width // 3
        draw.rectangle([0, 0, band, height], fill=colors[0])
        draw.rectangle([band, 0, band * 2, height], fill=colors[1])
        draw.rectangle([band * 2, 0, width, height], fill=colors[2])
    else:
        band = height // max(len(colors), 1)
        for index, color in enumerate(colors):
            draw.rectangle([0, index * band, width, (index + 1) * band], fill=color)

    image.save(path, format='PNG')
    return path


def ensure_default_languages():
    """Create/update default language cards with PNG images and English first."""
    from .models import ChatTemplateLanguage

    for item in DEFAULT_LANGUAGES:
        language = ChatTemplateLanguage.objects.filter(code=item['code']).first()
        if language is None:
            for legacy in item.get('legacy_codes', ()):
                language = ChatTemplateLanguage.objects.filter(code=legacy).first()
                if language is not None:
                    break

        if language is None:
            language = ChatTemplateLanguage(
                code=item['code'],
                name=item['name'],
                language_name=item['language_name'],
                sort_order=item['sort_order'],
            )
            language.save()
        else:
            language.code = item['code']
            language.name = item['name']
            language.language_name = item['language_name']
            language.sort_order = item['sort_order']
            language.save()

        if not language.image:
            png_path = _write_default_flag_png(item['code'], item['flag_colors'])
            # File already lives in the language image storage directory.
            language.image.name = png_path.name
            language.save(update_fields=['image'])
