import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0004_procedureimage_titled_pairs'),
    ]

    operations = [
        migrations.CreateModel(
            name='GallerySection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('procedure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_sections', to='clinic.procedure')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='SectionImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(max_length=120)),
                ('title_tr', models.CharField(max_length=120, blank=True)),
                ('image', models.ImageField(upload_to='procedures/gallery/')),
                ('image_type', models.CharField(choices=[('before', 'Before'), ('after', 'After')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='clinic.gallerysection')),
            ],
            options={
                'ordering': ['image_type', 'created_at'],
            },
        ),
        migrations.DeleteModel(
            name='ProcedureImage',
        ),
    ]
