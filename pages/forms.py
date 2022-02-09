from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import ModelForm

from .models import *
from .choices import *


class OptionForm(ModelForm):
    sample_count = forms.NumberInput(attrs={'size': '3', 'label': 'Sample Count'})
    countdown_per_pic = forms.NumberInput(attrs={'size': '3'})
    headline_el = forms.CharField(required=True, label='Τίτλος αρχικής σελίδας')
    headline_en = forms.CharField(required=True, label='Start page title')
    footer_el = forms.CharField(required=True, label='Τμήμα υποσέλιδου')
    footer_en = forms.CharField(required=True, label='Footer section')
    instructions_el = forms.CharField(label='Οδηγίες', widget=CKEditorWidget(config_name='instruction'))
    instructions_en = forms.CharField(label='Instructions', widget=CKEditorWidget(config_name='instruction'))

    class Meta:
        model = Option
        fields = '__all__'


class PairForm(ModelForm):
    caption_pri_el = forms.CharField(label='Λεζάντα Αρχικής εικόνας', widget=CKEditorWidget(config_name='caption'))
    caption_pri_en = forms.CharField(label='Caption of Primary image', widget=CKEditorWidget(config_name='caption'))
    image_pri = forms.ImageField(required=True)
    caption_sec_el = forms.CharField(label='Λεζάντα Δευτερεύουσας εικόνας',
                                     widget=CKEditorWidget(config_name='caption'))
    caption_sec_en = forms.CharField(label='Caption of Secondary image', widget=CKEditorWidget(config_name='caption'))
    image_sec = forms.ImageField(required=True)
    description_el = forms.CharField(label='Επεξήγηση αντιστοίχισης', widget=CKEditorWidget(config_name='description'))
    description_en = forms.CharField(label='Matching explanation', widget=CKEditorWidget(config_name='description'))

    class Meta:
        model = Pair
        fields = {
            'caption_pri_el',
            'caption_pri_en',
            'image_pri',
            'caption_sec_el',
            'caption_sec_en',
            'image_sec',
            'description_el',
            'description_en',
        }

        exclude = [
            'width_pri',
            'height_pri',
            'width_sec',
            'height_sec'
        ]


class TargetForm(ModelForm):
    x_pri = forms.FloatField(required=True)
    y_pri = forms.FloatField(required=True)
    w_pri = forms.FloatField(required=True)
    h_pri = forms.FloatField(required=True)
    x_sec = forms.FloatField(required=False)
    y_sec = forms.FloatField(required=False)
    w_sec = forms.FloatField(required=False)
    h_sec = forms.FloatField(required=False)

    class Meta:
        model = Target
        exclude = ['pair']


class UserForm(ModelForm):
    # session = forms.CharField()
    gender = forms.ChoiceField(choices=gender, required=True, label='Φύλο / Gender')
    age = forms.ChoiceField(choices=age, required=True, label='Ηλικία / Age')
    education = forms.ChoiceField(choices=education, required=True, label='Επίπεδο Μόρφωσης / Education Level')
    sector = forms.CharField(required=True, label='Τομέας / Sector')
    knowledge = forms.ChoiceField(choices=knowledge, required=True, label='Γνώσεις της Ιστορίας της Τέχνης / Art '
                                                                          'History Knowledge')

    class Meta:
        model = User
        fields = '__all__'
