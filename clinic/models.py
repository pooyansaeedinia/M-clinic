from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

from .validators import validate_language_image_upload

language_image_storage = FileSystemStorage(
    location=settings.BASE_DIR / 'static' / 'portal' / 'languages',
    base_url=f'{settings.STATIC_URL}portal/languages/',
)


def language_image_upload_to(instance, filename):
    ext = Path(filename).suffix.lower().lstrip('.') or 'png'
    if ext == 'jpeg':
        ext = 'jpg'
    code = instance.code or 'language'
    return f'{code}.{ext}'


class ChatTemplateLanguage(models.Model):
    """Top-level language / market workspace for chat templates (portal CMS)."""

    name = models.CharField(
        max_length=120,
        help_text='Display name on the dashboard card, e.g. English.',
    )
    code = models.SlugField(
        max_length=64,
        unique=True,
        help_text='URL slug, e.g. english.',
    )
    language_name = models.CharField(
        max_length=120,
        blank=True,
        help_text='Optional secondary language label.',
    )
    image = models.ImageField(
        upload_to=language_image_upload_to,
        storage=language_image_storage,
        blank=True,
        validators=[validate_language_image_upload],
        help_text='PNG or JPG card image stored under static/portal/languages/.',
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    # Extensible bag for future fields without migrations.
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    @property
    def subtitle(self):
        label = self.language_name or self.name
        return f'{label} templates'

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return ''


class ChatTemplateSection(models.Model):
    """A titled message template within a language."""

    class TemplateType(models.TextChoices):
        MESSAGE = 'message', 'Message'
        # Reserved for future template kinds (snippets, macros, etc.).

    language = models.ForeignKey(
        ChatTemplateLanguage,
        on_delete=models.CASCADE,
        related_name='sections',
    )
    title = models.CharField(max_length=200)
    body = models.TextField(help_text='Template message text.')
    template_type = models.CharField(
        max_length=32,
        choices=TemplateType.choices,
        default=TemplateType.MESSAGE,
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=120, blank=True)
    tags = models.JSONField(default=list, blank=True)
    variables = models.JSONField(
        default=dict,
        blank=True,
        help_text='Named placeholders for future variable substitution.',
    )
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return f'{self.title} ({self.language.code})'


class Procedure(models.Model):
    slug = models.SlugField(unique=True)
    name_en = models.CharField(max_length=120)
    name_tr = models.CharField(max_length=120)
    summary_en = models.TextField()
    summary_tr = models.TextField()
    default_image = models.ImageField(upload_to='procedures/defaults/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name_en']

    def __str__(self):
        return self.name_en


class GallerySection(models.Model):
    procedure = models.ForeignKey(
        Procedure,
        on_delete=models.CASCADE,
        related_name='gallery_sections',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.procedure.name_en} section #{self.pk}'


class SectionImage(models.Model):
    class ImageType(models.TextChoices):
        BEFORE = 'before', 'Before'
        AFTER = 'after', 'After'

    section = models.ForeignKey(
        GallerySection,
        on_delete=models.CASCADE,
        related_name='images',
    )
    title_en = models.CharField(max_length=120)
    title_tr = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to='procedures/gallery/')
    image_type = models.CharField(max_length=10, choices=ImageType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['image_type', 'created_at']

    def __str__(self):
        return f'{self.title_en} ({self.image_type})'
