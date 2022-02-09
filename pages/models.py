from django.db import models
from .choices import *
from ckeditor.fields import RichTextField


# ------------- OPTION ------------- #
class Option(models.Model):
    sample_count = models.PositiveSmallIntegerField(default=15, blank=False, null=False)
    countdown_per_pic = models.PositiveSmallIntegerField(default=60, blank=False, null=False)
    language = models.CharField(max_length=2, choices=languages, default='EL')
    headline_el = models.CharField(max_length=25, default='Οδηγίες')
    headline_en = models.CharField(max_length=25, default='Instructions')
    instructions_el = RichTextField(default='Χώρος εισαγωγής οδηγιών/πληροφοριών.')
    instructions_en = RichTextField(default='Put your instructions here')
    footer_el = models.CharField(max_length=120, default='© 2020 Περικλής Περικλέους - Πανεπιστήμιο Πατρών')
    footer_en = models.CharField(max_length=120, default='© 2020 Periklis Perikleous - University of Patras')


# ------------- PAIR ------------- #
class Pair(models.Model):
    caption_pri_el = RichTextField(max_length=50, blank=False)
    caption_pri_en = RichTextField(max_length=50, blank=False)
    caption_sec_el = RichTextField(max_length=50, blank=False)
    caption_sec_en = RichTextField(max_length=50, blank=False)
    description_el = RichTextField(blank=True)
    description_en = RichTextField(blank=True)

    image_pri = models.ImageField(upload_to='', blank=False, max_length=100,
                                  height_field='height_pri', width_field='width_pri')
    height_pri = models.IntegerField(default=0)
    width_pri = models.IntegerField(default=0)

    image_sec = models.ImageField(upload_to='', blank=False, max_length=100,
                                  height_field='height_sec', width_field='width_sec')
    height_sec = models.IntegerField(default=0)
    width_sec = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Pairs"


# ------------- TARGET ------------- #
class Target(models.Model):
    pair = models.OneToOneField(Pair, related_name='pair_target', on_delete=models.CASCADE)
    x_pri = models.FloatField(verbose_name='x - primary', null=False)
    y_pri = models.FloatField(verbose_name='y - primary', null=False)
    w_pri = models.FloatField(verbose_name='width - primary', null=False)
    h_pri = models.FloatField(verbose_name='height - primary', null=False)
    x_sec = models.FloatField(verbose_name='x - secondary', null=True)
    y_sec = models.FloatField(verbose_name='y - secondary', null=True)
    w_sec = models.FloatField(verbose_name='width - secondary', null=True)
    h_sec = models.FloatField(verbose_name='height - secondary', null=True)


# ------------- USER ------------- #
class User(models.Model):
    session = models.IntegerField()
    gender = models.CharField(max_length=1, choices=gender)
    age = models.CharField(max_length=5, choices=age)
    education = models.CharField(max_length=11, choices=education)
    sector = models.CharField(max_length=40)
    knowledge = models.CharField(max_length=2, choices=knowledge)


# ------------- DATA ------------- #
class Data(models.Model):
    session = models.IntegerField()
    timestamp = models.CharField(max_length=50)
    status = models.CharField(max_length=10, blank=True, null=True)
    score = models.FloatField(null=True)
    pair = models.ForeignKey(Pair, related_name='pair_data', null=True, on_delete=models.CASCADE)
    filename_pri = models.CharField(max_length=120, blank=True, null=True)
    filename_sec = models.CharField(max_length=120, blank=True, null=True)
    xtl_pri = models.FloatField(null=True)
    ytl_pri = models.FloatField(null=True)
    xbr_pri = models.FloatField(null=True)
    ybr_pri = models.FloatField(null=True)
    xtl_sec = models.FloatField(null=True)
    ytl_sec = models.FloatField(null=True)
    xbr_sec = models.FloatField(null=True)
    ybr_sec = models.FloatField(null=True)
    countdown_per_pic = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = "Data"


# ------------- RANK ------------- #
class Rank(models.Model):
    session = models.IntegerField()
    pair = models.PositiveSmallIntegerField()
    success = models.PositiveSmallIntegerField()
    failure = models.PositiveSmallIntegerField()
    # total_score = models.FloatField(null=True)
    accuracy = models.FloatField(null=True)
    response = models.FloatField(null=True)

    class Meta:
        verbose_name_plural = "Rank"
