# file/widgets.py

from django_select2.forms import ModelSelect2MultipleWidget
from taggit.models import Tag

class ColorTagSelect2Widget(ModelSelect2MultipleWidget):
    model = Tag
    search_fields = ['name__icontains']
    attrs = {'data-placeholder': 'Select or create tags'}

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs.update({'data-color': self.model.color})
        return attrs
