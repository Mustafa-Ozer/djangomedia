# Generated by Django 3.0.4 on 2020-04-02 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='Comment_date',
            new_name='comment_date',
        ),
    ]
