from django.contrib import admin
from django.utils.html import mark_safe

from epi.models import Sala, Tipo, Tamanho, EspessuraPb, EPI, Verificacao, Image
from epi.forms import EPIForm


# Register your models here.
class SalaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nome')


class TipoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nome', 'abreviatura')


class TamanhoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'designacao')


class EspessuraPbAdmin(admin.ModelAdmin):
    list_display = ('pk', 'valor')


class EPIAdmin(admin.ModelAdmin):
    form = EPIForm
    list_display = (
        'slug', 'sala', 'tipo', 'marca', 'modelo', 'cor', 'tamanho', 'genero', 'utilizacao', 'referencia', 'espessuraPb', 'norma',
        'data')
    list_filter = ('sala', 'tipo', 'marca', 'espessuraPb', 'utilizacao')
    list_display_links = ('slug',)
    # list_editable = ('sala',)
    list_select_related = ('sala', 'tipo')
    ordering = ('pk',)
    search_fields = ('slug',)
    preserve_filters = True
    # exclude = ('designacao',)


class ImagesInline(admin.TabularInline):
    model = Image


class VerificacaoAdmin(admin.ModelAdmin):
    list_display = (
    'pk', 'epi', 'sala', 'acondicionamento', 'conservacao', 'fitavelcro', 'limpeza', 'data', 'utilizador', 'obs')
    list_filter = ('epi__tipo', 'data')
    list_display_links = ('pk',)
    # list_editable = ('sala',)
    # list_select_related = ('sala', 'tipo')
    ordering = ('pk',)
    search_fields = ('epi',)
    list_per_page = 10
    preserve_filters = True
    inlines = [ImagesInline]


class ImageAdmin(admin.ModelAdmin):

    def image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image.url,
            width=obj.image.width,
            height=obj.image.height,
            )
    )


admin.site.register(Sala, SalaAdmin)
admin.site.register(Tipo, TipoAdmin)
admin.site.register(Tamanho, TamanhoAdmin)
admin.site.register(EspessuraPb, EspessuraPbAdmin)
admin.site.register(EPI, EPIAdmin)
admin.site.register(Verificacao, VerificacaoAdmin)
admin.site.register(Image, ImageAdmin)
