from django.db import migrations, models


def clear_gallery(apps, schema_editor):
    ProcedureImage = apps.get_model('clinic', 'ProcedureImage')
    ProcedureImage.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0003_gallery_multiple_images'),
    ]

    operations = [
        migrations.RunPython(clear_gallery, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='procedureimage',
            name='image',
        ),
        migrations.RemoveField(
            model_name='procedureimage',
            name='image_type',
        ),
        migrations.AddField(
            model_name='procedureimage',
            name='after_image',
            field=models.ImageField(upload_to='procedures/after/'),
        ),
        migrations.AddField(
            model_name='procedureimage',
            name='before_image',
            field=models.ImageField(upload_to='procedures/before/'),
        ),
        migrations.AddField(
            model_name='procedureimage',
            name='title_en',
            field=models.CharField(default='Case', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='procedureimage',
            name='title_tr',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AlterModelOptions(
            name='procedureimage',
            options={'ordering': ['-created_at']},
        ),
    ]
