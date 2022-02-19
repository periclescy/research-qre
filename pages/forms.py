from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import ModelForm

from .models import *
from .choices import *


class OptionForm(ModelForm):
    headline = forms.CharField(required=True, label='Start page title')
    footer = forms.CharField(required=True, label='Footer section')
    instructions = forms.CharField(label='Instructions', widget=CKEditorWidget(config_name='instruction'))

    class Meta:
        model = Option
        fields = '__all__'


class UserForm(ModelForm):
    # session = forms.CharField()
    gender = forms.ChoiceField(choices=gender, required=True, label='Φύλο / Gender')
    age = forms.ChoiceField(choices=age, required=True, label='Ηλικία / Age')
    education = forms.ChoiceField(choices=education, required=True, label='Επίπεδο Μόρφωσης / Education Level')
    # district = forms.CharField(choices=district, required=True, label='Επαρχία / District')
    residence = forms.ChoiceField(choices=residence, required=True, label='Διαμονή / Residence')

    class Meta:
        model = User
        fields = '__all__'


class QuestionForm(ModelForm):
    question = forms.CharField(label='Question', widget=CKEditorWidget(config_name='question'))
    answer_category = forms.ChoiceField(choices=answer_category, required=True, label='Answer Category')

    class Meta:
        model = User
        fields = '__all__'
