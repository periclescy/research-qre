from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import ModelForm

from .models import *


class OptionForm(ModelForm):
    brake_time = forms.IntegerField(required=True)
    headline = forms.CharField(required=True, label='Start page title')
    footer = forms.CharField(required=True, label='Footer section')
    instructions = forms.CharField(label='Instructions', widget=CKEditorWidget(config_name='instruction'))

    class Meta:
        model = Option
        fields = '__all__'


class UserForm(ModelForm):
    # session = forms.CharField()
    team = forms.ChoiceField(choices=Team.choices, required=True, label='Ομάδα / Team')
    gender = forms.ChoiceField(choices=Gender.choices, required=True, label='Φύλο / Gender')
    age = forms.ChoiceField(choices=Age.choices, required=True, label='Ηλικία / Age')
    education = forms.ChoiceField(choices=Education.choices, required=True, label='Επίπεδο Μόρφωσης / Education Level')
    district = forms.ChoiceField(choices=District.choices, required=True, label='Επαρχία / District')
    residence = forms.ChoiceField(choices=Residence.choices, required=True, label='Διαμονή / Residence')

    class Meta:
        model = User
        fields = '__all__'


class SectionForm(ModelForm):
    section = forms.ChoiceField(choices=SectionCategory.choices, required=True, label='Section')
    answer_category = forms.ChoiceField(choices=AnswerCategory.choices, required=True, label='Answer Category')

    class Meta:
        model = Section
        fields = '__all__'


class QuestionForm(ModelForm):
    question = forms.CharField(label='Question', widget=CKEditorWidget(config_name='question'))

    class Meta:
        model = Question
        fields = '__all__'
