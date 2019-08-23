from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from epi.views import EPIListView, EPICreateView, EPIDetailView, EPIUpdateView, EPIDeleteView, VerificacaoCreateView, \
    VerificacaoDetailView, VerificacaoUpdateView, VerificacaoDeleteView, scanner_view

app_name = 'epi'
urlpatterns = [
    path('', EPIListView.as_view(), name='epi_list'),
    path('criar/', EPICreateView.as_view(), name='epi_create'),
    path('<slug:slug>/', EPIDetailView.as_view(), name='epi_detail'),
    path('<slug:slug>/Editar', EPIUpdateView.as_view(), name='epi_update'),
    path('<slug:slug>/Apagar/', EPIDeleteView.as_view(), name='epi_delete'),
    path('<slug:slug>/NovaVerificação', VerificacaoCreateView.as_view(), name='verif_create'),
    path('<slug:slug>/Verificação/<int:pk>', VerificacaoDetailView.as_view(), name='verif_detail'),
    path('<slug:slug>/Verificação/<int:pk>/Editar', VerificacaoUpdateView.as_view(), name='verif_update'),
    path('<slug:slug>/Verificação/<int:pk>/Apagar', VerificacaoDeleteView.as_view(), name='verif_delete'),
    path('scanner/teste/', scanner_view, name='scanner'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
