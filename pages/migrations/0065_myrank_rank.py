# Generated by Django 3.0.8 on 2020-11-16 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0064_auto_20201116_1910'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.IntegerField()),
                ('pair', models.PositiveSmallIntegerField()),
                ('success', models.PositiveSmallIntegerField()),
                ('failure', models.PositiveSmallIntegerField()),
                ('total_score', models.FloatField(null=True)),
                ('accuracy', models.FloatField(null=True)),
                ('response', models.FloatField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Rank',
            },
        ),
        migrations.CreateModel(
            name='MyRank',
            fields=[
            ],
            options={
                'verbose_name_plural': '~ Import/Export Rank',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('pages.data',),
        ),
    ]
