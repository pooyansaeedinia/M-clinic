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


class ProcedureImage(models.Model):
    procedure = models.ForeignKey(
        Procedure,
        on_delete=models.CASCADE,
        related_name='gallery_items',
    )
    before_image = models.ImageField(upload_to='procedures/before/')
    after_image = models.ImageField(upload_to='procedures/after/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.procedure.name_en} #{self.pk}'
