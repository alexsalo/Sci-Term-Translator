__author__ = 'alex'
from django import forms

SUPPORTED_PREFIXES = (
    ('ru', 'Russian'),
    ('en', 'English'),
    ('zh', 'Chinese'),
    ('de', 'German'),
    ('ar', 'Arabic'),
    ('cs', 'Czech'),
)

class searchForm(forms.Form):
    search_query = forms.CharField(label='Term', max_length=100, widget=forms.TextInput(
        attrs={'type':'search', 'id':'search', 'placeholder': 'Search...'}))
    #detected_lang = forms.MultipleChoiceField(choices=SUPPORTED_PREFIXES, label='Language Detected:')
    # = forms.ChoiceField(label='Select desired language')
    prefix = forms.MultipleChoiceField(choices=SUPPORTED_PREFIXES, widget=forms.RadioSelect(
        attrs={'type':'radio', 'id':'radio'}),
        initial='en')
    answer = forms.CharField(label='Answer', max_length=100, widget=forms.TextInput(
         attrs={'type':'search', 'id':'search', 'placeholder': 'Translation...'}))