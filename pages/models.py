from django.db import models
from ckeditor.fields import RichTextField


# *** *** Choices Classes *** *** #
class Team(models.TextChoices):
    null = '', "--"
    male = 'A', "Ομάδα Α / Team A"
    female = 'B', "Ομάδα B / Team B"


class Gender(models.TextChoices):
    null = '', "--"
    male = 'M', "Άρρεν / Male"
    female = 'F', "Θήλυ / Female"


class Age(models.TextChoices):
    null = '', "--"
    u17 = 'u17', "u17"
    r1825 = '18-25', "18-25"
    r2635 = '26-35', "26-35"
    r3645 = '36-45', "36-45"
    r4655 = '46-55', "46-55"
    r5664 = '56-64', "56-64"
    o65 = '65+', "65+"


class Education(models.TextChoices):
    null = '', "--"
    gymnasium = "gymnasium", "Γυμνάσιο / Gymnasium"
    lyceum = "lyceum", "Λύκειο - Τεχνική Σχολή / Lyceum"
    BSc = "BSc", "Πτυχίο / Bachelor"
    MSc = "MSc", "Μεταπτυχιακό / Master's"
    PhD = "PhD", "Διδακτορικό / Doctorate"


class District(models.TextChoices):
    null = '', "--"
    lemesos = "lemesos", "Λεμεσός / Lemesos"
    nicosia = "nicosia", "Λευκωσία / Nicosia"
    larnaca = "larnaca", "Λάρνακα / Larnaca"
    paphos = "paphos", "Πάφος / Paphos"
    ammochostos = "ammochostos", "Αμμόχωστος / Ammochostos"
    kyrenia = "kyrenia", "Κερύνεια / Kyrenia"


class Residence(models.TextChoices):
    null = '', "--"
    city = "city", "Πόλη / City"
    suburb = "suburb", "Προάστιο / Suburb"
    village = "village", "Χωριό / Village"


class SectionCategory(models.TextChoices):
    null = '', "--"
    a = "A", "A"
    b = "B", "B"
    c = "C", "C"
    d = "D", "D"
    e = "E", "E"


class AnswerCategory(models.TextChoices):
    null = '', "--"
    boolean = "boolean", "True / False"
    likert6 = "likert6", "6 point Likert"
    likert7 = "likert7", "7 point Likert"
    brake1 = "brake1", "1 min brake"
    brake2 = "brake2", "2 min brake"
    brake5 = "brake5", "5 min brake"
    brake10 = "brake10", "10 min brake"
    brake15 = "brake15", "15 min brake"


# *** *** End of Choices Classes *** *** #


# ------------- OPTION ------------- #
class Option(models.Model):
    headline = models.CharField(max_length=25, default='Instructions')
    instructions = RichTextField(default='Put your instructions here')
    footer = models.CharField(max_length=120, default='© 2022 Regnabytes Ltd')


# ------------- USER ------------- #
class User(models.Model):
    session = models.IntegerField()
    team = models.CharField(max_length=1, choices=Team.choices, default=Team.null)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.null)
    age = models.CharField(max_length=5, choices=Age.choices, default=Age.null)
    education = models.CharField(max_length=10, choices=Education.choices, default=Education.null)
    district = models.CharField(max_length=12, choices=District.choices, default=District.null)
    residence = models.CharField(max_length=12, choices=Residence.choices, default=Residence.null)


# ------------- SECTION ------------- #
class Section(models.Model):
    section = models.CharField(max_length=1, choices=SectionCategory.choices, default=SectionCategory.null, unique=True)
    answer_category = models.CharField(max_length=8, choices=AnswerCategory.choices, default=AnswerCategory.null)

    def __str__(self):
        return str(self.section)


# ------------- QUESTION ------------- #
class Question(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    question = RichTextField(max_length=1500, blank=False)


# ------------- DATA ------------- #
class Data(models.Model):
    session = models.IntegerField()
    timestamp = models.CharField(max_length=50)
    status = models.CharField(max_length=10, null=True)
    question = RichTextField(max_length=1500, null=True)
    selection = models.IntegerField(null=True)
    team = models.CharField(max_length=30, null=True)

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
