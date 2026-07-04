from django import forms

from .models import GallerySection, Procedure, SectionImage


class ProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedure
        fields = [
            'slug',
            'name_en',
            'name_tr',
            'summary_en',
            'summary_tr',
            'default_image',
        ]
        labels = {
            'slug': 'Slug (url name)',
            'name_en': 'Procedure Name (English)',
            'name_tr': 'Procedure Name (Turkish)',
            'summary_en': 'Description (English)',
            'summary_tr': 'Description (Turkish)',
            'default_image': 'Default Procedure Image',
        }


class SectionImageForm(forms.ModelForm):
    class Meta:
        model = SectionImage
        fields = [
            'title_en',
            'title_tr',
            'image',
            'image_type',
        ]
        labels = {
            'title_en': 'Title (English)',
            'title_tr': 'Title (Turkish)',
            'image': 'Image',
            'image_type': 'Type',
        }
