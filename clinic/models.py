from django.db import models


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
