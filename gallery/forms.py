from datetime import datetime

from django.forms import ModelForm, Textarea, forms


from gallery.models import Comment, Picture
from django import forms

DISPLAY_CHOICES = (
    ('1', 'Yes'),
    ('0', 'No')
)


class CommentsForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comments']
        widgets = {
            'comments': Textarea(attrs={'cols': 40, 'rows': 2}),
        }


class PictureForm(forms.Form):
    file = forms.ImageField()
    check = forms.ChoiceField(widget=forms.RadioSelect, choices=DISPLAY_CHOICES)
    name_of_picture = forms.CharField(label="Picture name", max_length= 50)


