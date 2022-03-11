# Generated by Django 3.2 on 2022-03-11 09:02

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20220311_1059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.IntegerField()),
                ('timestamp', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=10, null=True)),
                ('section', models.CharField(max_length=1, null=True)),
                ('question', ckeditor.fields.RichTextField(max_length=1500, null=True)),
                ('selection', models.IntegerField(null=True)),
                ('team', models.CharField(max_length=30, null=True)),
            ],
            options={
                'verbose_name_plural': 'Data',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.IntegerField()),
                ('team', models.CharField(choices=[('', '--'), ('A', 'Ομάδα Α / Team A'), ('B', 'Ομάδα B / Team B')], default='', max_length=1)),
                ('gender', models.CharField(choices=[('', '--'), ('M', 'Άρρεν / Male'), ('F', 'Θήλυ / Female')], default='', max_length=1)),
                ('age', models.CharField(choices=[('', '--'), ('u17', 'u17'), ('18-25', '18-25'), ('26-35', '26-35'), ('36-45', '36-45'), ('46-55', '46-55'), ('56-64', '56-64'), ('65+', '65+')], default='', max_length=5)),
                ('education', models.CharField(choices=[('', '--'), ('gymnasium', 'Γυμνάσιο / Gymnasium'), ('lyceum', 'Λύκειο - Τεχνική Σχολή / Lyceum'), ('BSc', 'Πτυχίο / Bachelor'), ('MSc', "Μεταπτυχιακό / Master's"), ('PhD', 'Διδακτορικό / Doctorate')], default='', max_length=10)),
                ('district', models.CharField(choices=[('', '--'), ('lemesos', 'Λεμεσός / Lemesos'), ('nicosia', 'Λευκωσία / Nicosia'), ('larnaca', 'Λάρνακα / Larnaca'), ('paphos', 'Πάφος / Paphos'), ('ammochostos', 'Αμμόχωστος / Ammochostos'), ('kyrenia', 'Κερύνεια / Kyrenia')], default='', max_length=12)),
                ('residence', models.CharField(choices=[('', '--'), ('city', 'Πόλη / City'), ('suburb', 'Προάστιο / Suburb'), ('village', 'Χωριό / Village')], default='', max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='MyData',
            fields=[
            ],
            options={
                'verbose_name_plural': '~ Import/Export Data',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('pages.data',),
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
            ],
            options={
                'verbose_name_plural': '~ Import/Export Users',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('pages.user',),
        ),
    ]