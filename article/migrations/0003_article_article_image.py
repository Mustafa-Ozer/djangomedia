# Generated by Django 3.0.4 on 2020-04-01 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20200401_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article_image',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Fotoğraf Ekle'),
        ),
    ]