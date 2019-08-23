from django import forms
from django.forms.models import inlineformset_factory

from epi.models import EPI, Verificacao, Image


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"


class EPIForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(EPIForm, self).__init__(*args, **kwargs)
        self.fields['cor'].widget.attrs['class'] = None

    class Meta:
        model = EPI
        fields = ['estado', 'sala', 'tipo', 'marca', 'modelo', 'cor', 'tamanho', 'genero', 'referencia', 'espessuraPb',
                  'utilizacao', 'norma', 'data',]
        widgets = {
            'cor': forms.TextInput(attrs={'type': 'color'}),
        }


class VericacaoForm(BaseForm):
    def __init__(self, *args, **kwargs):
        epi = kwargs.pop('epi', None)
        user = kwargs.pop('user', None)
        super(VericacaoForm, self).__init__(*args, **kwargs)
        self.fields['epi'].initial = epi
        self.fields['utilizador'].initial = user

    class Meta:
        model = Verificacao
        fields = '__all__'
        widgets = {
            'epi': forms.HiddenInput,
            'utilizador': forms.HiddenInput,
        }


class ImageForm(BaseForm):
    class Meta:
        model = Image
        fields = '__all__'


ImagesFormSet = inlineformset_factory(Verificacao, Image, form=ImageForm, extra=1, can_delete=True)
