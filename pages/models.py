from django.db import models
from .choices import *
from ckeditor.fields import RichTextField


# ------------- OPTION ------------- #
class Option(models.Model):
    headline = models.CharField(max_length=25, default='Instructions')
    instructions = RichTextField(default='Put your instructions here')
    footer = models.CharField(max_length=120, default='© 2022 Regnabytes Ltd')


# ------------- USER ------------- #
class User(models.Model):
    session = models.IntegerField()
    gender = models.CharField(max_length=1, choices=gender)
    age = models.CharField(max_length=5, choices=age)
    education = models.CharField(max_length=30, choices=education)
    district = models.CharField(max_length=30, choices=district)
    residence = models.CharField(max_length=30, choices=residence)


# ------------- QUESTION ------------- #
class Question(models.Model):
    question = RichTextField(max_length=500, blank=False)
    answer_category = models.CharField(max_length=30, choices=answer_category)


# ------------- DATA ------------- #
class Data(models.Model):
    session = models.IntegerField()
    timestamp = models.CharField(max_length=50)
    status = models.CharField(max_length=10, blank=True, null=True)
    answer = models.CharField(max_length=1)

    class Meta:
        verbose_name_plural = "Data"


# ------------- RANK ------------- #
# class Rank(models.Model):
#     session = models.IntegerField()
#     pair = models.PositiveSmallIntegerField()
#     success = models.PositiveSmallIntegerField()
#     failure = models.PositiveSmallIntegerField()
#     # total_score = models.FloatField(null=True)
#     accuracy = models.FloatField(null=True)
#     response = models.FloatField(null=True)
#
#     class Meta:
#         verbose_name_plural = "Rank"
