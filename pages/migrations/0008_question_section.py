# Generated by Django 3.2 on 2022-02-20 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_auto_20220220_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='section',
            field=models.CharField(choices=[('', '--'), ('a', 'A'), ('b', 'B')], default='', max_length=1),
        ),
    ]
