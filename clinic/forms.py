from django import forms

from .models import Procedure, ProcedureImage


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


class ProcedureImageForm(forms.ModelForm):
    class Meta:
        model = ProcedureImage
        fields = [
            'before_image',
            'after_image',
        ]
        labels = {
            'before_image': 'Before Image',
            'after_image': 'After Image',
        }
