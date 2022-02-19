from django.db import models
from ckeditor.fields import RichTextField


# *** *** Choices Classes *** *** #

class Gender(models.TextChoices):
    DEF = '', "--"
    Male = 'M', "Άρρεν / Male"
    Female = 'F', "Θήλυ / Female"


class Age(models.TextChoices):
    DEF = '', "--"
    u17 = 'u17', "u17"
    r1825 = '18-25', "18-25"
    r2635 = '26-35', "26-35"
    r3645 = '36-45', "36-45"
    r4655 = '46-55', "46-55"
    r5664 = '56-64', "56-64"
    o65 = '65+', "65+"


class Education(models.TextChoices):
    DEF = '', "--"
    gymnasium = "gymnasium", "Γυμνάσιο / Gymnasium"
    lyceum = "lyceum", "Λύκειο - Τεχνική Σχολή / Lyceum"
    BSc = "BSc", "Πτυχίο / Bachelor"
    MSc = "MSc", "Μεταπτυχιακό / Master's"
    PhD = "PhD", "Διδακτορικό / Doctorate"


class District(models.TextChoices):
    DEF = '', "--"
    lemesos = "lemesos", "Λεμεσός/ Λεμεσός"
    nicosia = "nicosia", "Λευκωσία / Nicosia"
    larnaca = "larnaca", "Λάρνακα / Larnaca"
    paphos = "paphos", "Πάφος / Paphos"
    ammochostos = "ammochostos", "Αμμόχωστος / Ammochostos"
    kyrenia = "kyrenia", "Κερύνεια / Kyrenia"


class Residence(models.TextChoices):
    DEF = '', "--"
    city = "city", "Πόλη / City"
    suburb = "suburb", "Προάστιο / Suburb"
    village = "village", "Χωριό / Village"


class AnswerCategory(models.TextChoices):
    boolean = "boolean", "True / False"
    likert6 = "likert6", "6 point Likert"
    likert7 = "likert7", "7 point Likert"


# *** *** End of Choices Classes *** *** #


# ------------- OPTION ------------- #
class Option(models.Model):
    headline = models.CharField(max_length=25, default='Instructions')
    instructions = RichTextField(default='Put your instructions here')
    footer = models.CharField(max_length=120, default='© 2022 Regnabytes Ltd')


# ------------- USER ------------- #
class User(models.Model):
    session = models.IntegerField()
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.DEF)
    age = models.CharField(max_length=5, choices=Age.choices, default=Age.DEF)
    education = models.CharField(max_length=10, choices=Education.choices, default=Education.DEF)
    district = models.CharField(max_length=12, choices=District.choices, default=District.DEF)
    residence = models.CharField(max_length=12, choices=Residence.choices, default=Residence.DEF)


# ------------- QUESTION ------------- #
class Question(models.Model):
    question = RichTextField(max_length=500, blank=False)
    answer_category = models.CharField(max_length=8, choices=AnswerCategory.choices, default=AnswerCategory.boolean)


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
