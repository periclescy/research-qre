# Generated by Django 3.0.6 on 2020-05-09 15:25

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0015_auto_20200430_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pair',
            name='caption_pri_el',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='pair',
            name='caption_pri_en',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='pair',
            name='caption_sec_el',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='pair',
            name='caption_sec_en',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
