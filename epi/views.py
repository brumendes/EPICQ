from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, PermissionDenied
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.template.defaultfilters import slugify
from django.core import serializers
from django.db import transaction
from django.contrib import messages

from epi.models import EPI, Sala, Tipo, Verificacao
from epi.forms import EPIForm, VericacaoForm, ImagesFormSet
from epi.filters import EPIFilter, VerifFilter


# Create your views here.
class EPIListView(LoginRequiredMixin, ListView):
    template_name = 'epi/epi_list.html'
    model = EPI
    order_by = 'sala'

    def get_context_data(self, **kwargs):
        context = super(EPIListView, self).get_context_data(**kwargs)
        context['filter'] = EPIFilter(self.request.GET, queryset=self.get_queryset())
        context['salas'] = Sala.objects.all()
        context['tipos'] = Tipo.objects.all()
        return context


def scanner_view(request):
    if request.is_ajax():
        barcode = request.GET.get('barcode', None)
        barcode_array = barcode.split(" ' ")
        slug = slugify(barcode_array[1] + "-" + "26")
        data = {
            'filter': serializers.serialize("json", EPI.objects.filter(slug=slug))
        }
    else:

        data = {
            'filter': "Não encontrado."
        }
    return JsonResponse(data)


class EPICreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'epi.add_epi'
    permission_denied_message = "Não tem permissões para efectuar a operação!"
    template_name = 'epi/epi_create.html'
    model = EPI
    form_class = EPIForm
    success_message = "Protector criado com sucesso!"
    success_url = reverse_lazy('epi:epi_list')

    def handle_no_permission(self):
        message = self.get_permission_denied_message()
        if self.raise_exception:
            raise PermissionDenied(message)
        messages.error(self.request, message)
        return redirect(self.success_url)


class EPIDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    template_name = 'epi/epi_detail.html'
    model = EPI

    def get_context_data(self, **kwargs):
        context = super(EPIDetailView, self).get_context_data()
        context['filter'] = VerifFilter(self.request.GET, queryset=self.object.verif_epis.all())
        context['latest_ver'] = self.object.get_latest_ver()
        return context


class EPIUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'epi.change_epi'
    permission_denied_message = "Não tem permissões para efectuar a operação!"
    template_name = 'epi/epi_update.html'
    model = EPI
    form_class = EPIForm
    success_message = "Protector alterado com sucesso!"

    def handle_no_permission(self):
        message = self.get_permission_denied_message()
        if self.raise_exception:
            raise PermissionDenied(message)
        messages.error(self.request, message)
        return redirect(self.get_object().get_absolute_url())


class EPIDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'epi.delete_epi'
    permission_denied_message = "Não tem permissões para efectuar a operação!"
    template_name = 'epi/epi_delete.html'
    model = EPI
    success_message = "EPI removido!"
    success_url = reverse_lazy('epi:epi_list')

    def handle_no_permission(self):
        message = self.get_permission_denied_message()
        if self.raise_exception:
            raise PermissionDenied(message)
        messages.error(self.request, message)
        return redirect(self.get_object().get_absolute_url())


class VerificacaoCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'epi.add_verificacao'
    permission_denied_message = "Não tem permissões para efectuar a operação!"
    template_name = 'epi/verif_create.html'
    model = Verificacao
    form_class = VericacaoForm
    success_message = "Verificação criada com sucesso!"

    def get_context_data(self, **kwargs):
        context = super(VerificacaoCreateView, self).get_context_data()
        epi = get_object_or_404(EPI, slug=self.kwargs['slug'])
        context['filter'] = EPIFilter(self.request.GET, queryset=self.get_queryset())
        if self.request.POST:
            context['formset'] = ImagesFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = ImagesFormSet()
        context['epi'] = epi
        return context

    def get_form_kwargs(self):
        kwargs = super(VerificacaoCreateView, self).get_form_kwargs()
        epi = get_object_or_404(EPI, slug=self.kwargs['slug'])
        user = self.request.user
        kwargs['epi'] = epi
        kwargs['user'] = user
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        form = self.get_form()
        formset = context['formset']
        with transaction.atomic():
            if formset.is_valid():
                self.object = form.save()
                formset.instance = self.object
                formset.save()
        return super(VerificacaoCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('epi:epi_detail', kwargs={'slug': self.kwargs['slug']})

    def handle_no_permission(self):
        message = self.get_permission_denied_message()
        if self.raise_exception:
            raise PermissionDenied(message)
        messages.error(self.request, message)
        return redirect(self.get_success_url())


class VerificacaoDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    template_name = 'epi/verif_detail.html'
    model = Verificacao


class VerificacaoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'epi.change_verificacao'
    permission_denied_message = "Não tem permissões para efectuar a operação!"
    template_name = 'epi/verif_update.html'
    model = Verificacao
    form_class = VericacaoForm
    success_message = "Verificação alterada com sucesso!"

    def get_context_data(self, **kwargs):
        context = super(VerificacaoUpdateView, self).get_context_data()
        if self.request.POST:
            context['formset'] = ImagesFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = ImagesFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form = self.get_form()
        formset = context['formset']
        with transaction.atomic():
            if formset.is_valid():
                self.object = form.save()
                formset.instance = self.object
                formset.save()
        return super(VerificacaoUpdateView, self).form_valid(form)

    def handle_no_permission(self):
        message = self.get_permission_denied_message()
        if self.raise_exception:
            raise PermissionDenied(message)
        messages.error(self.request, message)
        return redirect(self.get_object().get_absolute_url())


class VerificacaoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'epi.delete_verificacao'
    permission_denied_message = "Não tem permissões para efectuar a operação!"
    template_name = 'epi/verif_delete.html'
    model = Verificacao
    success_message = "Verificacao removida!"

    def get_success_url(self):
        return self.object.epi.get_absolute_url()

    def handle_no_permission(self):
        message = self.get_permission_denied_message()
        if self.raise_exception:
            raise PermissionDenied(message)
        messages.error(self.request, message)
        return redirect(self.get_object().get_absolute_url())
