from django.db import migrations, models


def clear_gallery(apps, schema_editor):
    ProcedureImage = apps.get_model('clinic', 'ProcedureImage')
    ProcedureImage.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0002_alter_procedureimage_options_and_more'),
    ]

    operations = [
        migrations.RunPython(clear_gallery, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='procedureimage',
            name='after_image',
        ),
        migrations.RemoveField(
            model_name='procedureimage',
            name='before_image',
        ),
        migrations.AddField(
            model_name='procedureimage',
            name='image',
            field=models.ImageField(upload_to='procedures/gallery/'),
        ),
        migrations.AddField(
            model_name='procedureimage',
            name='image_type',
            field=models.CharField(
                choices=[('before', 'Before'), ('after', 'After')],
                max_length=10,
            ),
        ),
        migrations.AlterModelOptions(
            name='procedureimage',
            options={'ordering': ['image_type', '-created_at']},
        ),
    ]
