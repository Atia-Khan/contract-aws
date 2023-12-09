# file/forms.py
from django import forms
from taggit.forms import TagField
from .models import File
from taggit.models import Tag
from .widgets import ColorTagSelect2Widget

class FileForm(forms.ModelForm):
    existing_tags = forms.MultipleChoiceField(
        required=False,
        widget=ColorTagSelect2Widget,
        choices=[(tag.slug, tag.name) for tag in Tag.objects.all()],
        label="Existing Tags"
    )
    new_tag = forms.CharField(max_length=50, required=False, label="Create a New Tag")

    class Meta:
        model = File
        fields = ['folder', 'file', 'existing_tags', 'new_tag']
        widgets = {'folder': forms.HiddenInput(), }
        required = {'folder': False}
        labels = {'folder': ''}
