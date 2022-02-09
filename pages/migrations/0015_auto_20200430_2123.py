# Generated by Django 3.0.5 on 2020-04-30 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_auto_20200430_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='target',
            name='h_sec',
            field=models.FloatField(null=True, verbose_name='height - secondary'),
        ),
        migrations.AlterField(
            model_name='target',
            name='w_sec',
            field=models.FloatField(null=True, verbose_name='width - secondary'),
        ),
        migrations.AlterField(
            model_name='target',
            name='x_sec',
            field=models.FloatField(null=True, verbose_name='x - secondary'),
        ),
        migrations.AlterField(
            model_name='target',
            name='y_sec',
            field=models.FloatField(null=True, verbose_name='y - secondary'),
        ),
    ]
