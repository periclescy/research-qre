# Generated by Django 3.0.6 on 2020-05-31 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0035_data_mydata_myrank_rank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='pair',
        ),
        migrations.DeleteModel(
            name='Rank',
        ),
        migrations.DeleteModel(
            name='MyData',
        ),
        migrations.DeleteModel(
            name='MyRank',
        ),
        migrations.DeleteModel(
            name='Data',
        ),
    ]
