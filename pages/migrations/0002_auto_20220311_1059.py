# Generated by Django 3.2 on 2022-03-11 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Data',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='MyData',
        ),
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]
