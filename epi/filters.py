from django_filters import FilterSet, DateFromToRangeFilter, CharFilter, DateFilter
from django_filters.widgets import RangeWidget, LinkWidget
from django import forms
from django.template.defaultfilters import slugify

from epi.models import EPI, Verificacao


class BaseFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super(FilterSet, self).__init__(*args, **kwargs)
        for field in self.form:
            field.field.widget.attrs['class'] = "form-control"


class EPIFilter(BaseFilter):
    slug = CharFilter(label="Designação")
    range = DateFromToRangeFilter(field_name='verif_epis__data', label='Intervalo de verificações', widget=RangeWidget(attrs={'type': 'date'}))

    class Meta:
        model = EPI
        fields = ['sala', 'tipo', 'slug', 'range']


class VerifFilter(BaseFilter):
    data = DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))

    class Meta:
        model = Verificacao
        fields = ['data']
