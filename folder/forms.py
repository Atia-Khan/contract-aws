from django.forms import ModelForm

from folder.models import Folder


class FolderForm(ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'text_color', 'parent']
