# Generated by Django 3.2 on 2022-02-19 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('M', 'Άρρεν / Male'), ('F', 'Θήλυ / Female')], default='', max_length=2),
        ),
    ]
