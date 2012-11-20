# -*- coding: utf-8 -*-
from django.views.generic.edit import ProcessFormView, ModelFormMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.template.context import RequestContext
from forms import PessoaForm
from models import Pessoa, Endereco
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class PessoaMixin(ModelFormMixin):
    form_class = PessoaForm
    model = Pessoa
    success_url = '/'

    def __init__(self, *args, **kwargs):
        super(PessoaMixin, self).__init__(*args, **kwargs)
        self.object = None

    def get_formset_queryset(self, formset):
        return formset.model.objects.filter(pessoa=self.object)

    def get_formsets(self):
        formsets = []
        if self.request.POST:
            for index, formset in enumerate(self.form_class.inlines):
                if self.object:
                    formsets.append(formset(self.request.POST, queryset=self.get_formset_queryset(formset), prefix='fs%s'%index))
                else:
                    formsets.append(formset(self.request.POST, queryset=formset.model.objects.none(), prefix='fs%s'%index))
        else:
            for index, formset in enumerate(self.form_class.inlines):
                if self.object:
                    formsets.append(formset(queryset=self.get_formset_queryset(formset), prefix='fs%s'%index))
                else:
                    formsets.append(formset(queryset=formset.model.objects.none(), prefix='fs%s'%index))
        return formsets

    def form_valid(self, form):
        self.object = form.save(commit=False)
        context = self.get_context_data()
        formsets = context['formsets']
        self.object.save()
        for object in formsets[0].save():
            self.object.enderecos.add(object) 
        for object in formsets[1].save():
            self.object.telefones.add(object)
        for object in formsets[2].save():
            self.object.emails.add(object)
        for object in formsets[3].save():
            self.object.contatos.add(object)
        form.save_m2m()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formsets):
        return self.render_to_response(self.get_context_data(form=form,
                                        formsets=formsets))

    def post(self, request, *args, **kwargs):
        self.object = 'pk' in self.kwargs and self.get_object() or None
        form_class = self.get_form_class()
        form = self.get_form(self.form_class)
        context = self.get_context_data()
        formsets = context['formsets']
        form_is_valid = form.is_valid() 
        for formset in formsets:
            form_is_valid = form_is_valid and formset.is_valid()
        if form_is_valid:
            return self.form_valid(form)
        else:
            return self.form_invalid(form, formsets)


class PessoaCreateView(PessoaMixin, CreateView):
    pass

class PessoaUpdateView(PessoaMixin, UpdateView):
    pass

class PessoaDeleteView(DeleteView):
    model = Pessoa
    success_url = "/"

class PessoaListView(ListView):
    model = Pessoa
