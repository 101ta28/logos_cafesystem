# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView
from pure_pagination.mixins import PaginationMixin

from .filters import InvoiceFilter
from .forms import InvoiceDetailFormSet, InvoiceForm
from .models import Invoice


class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, "is_update_view", False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def post(self, request, *args, **kwargs):
        if getattr(self, "is_update_view", False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {"instance": self.object}
        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


class InvoiceMixin(object):
    def form_valid(self, form, formset):

        # formset.save??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
        for detail_form in formset.forms:
            if detail_form.cleaned_data:
                detail_form.has_changed = lambda: True

        # ???????????????????????????
        invoice = form.save(commit=False)
        formset.instance = invoice
        details = formset.save(commit=False)

        sub_total = 0

        # ?????????????????????????????????
        for detail in details:
            detail.unit_price = detail.item.unit_price
            detail.amount = detail.unit_price * detail.quantity
            sub_total += detail.amount

        # ??????????????????????????????????????????????????????
        total_amount = sub_total

        invoice.sub_total = sub_total
        invoice.total_amount = total_amount
        invoice.created_by = self.request.user

        # DB??????
        with transaction.atomic():
            invoice.save()
            formset.instance = invoice
            formset.save()

        # ????????????????????????????????????
        return redirect(invoice.get_absolute_url())


class InvoiceFilterView(LoginRequiredMixin, PaginationMixin, FilterView):
    model = Invoice
    filterset_class = InvoiceFilter
    # ???????????????????????????????????????????????????
    queryset = Invoice.objects.all().order_by("-created_at")

    # pure_pagination?????????
    paginate_by = 10
    object = Invoice

    # ?????????????????????????????????????????????
    def get(self, request, **kwargs):
        if request.GET:
            request.session["query"] = request.GET
        else:
            request.GET = request.GET.copy()
            if "query" in request.session.keys():
                for key in request.session["query"].keys():
                    request.GET[key] = request.session["query"][key]

        return super().get(request, **kwargs)


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice


class InvoiceCreateView(LoginRequiredMixin, InvoiceMixin, FormsetMixin, CreateView):
    template_name = "invoice/invoice_form.html"
    model = Invoice
    form_class = InvoiceForm
    formset_class = InvoiceDetailFormSet


class InvoiceUpdateView(LoginRequiredMixin, InvoiceMixin, FormsetMixin, UpdateView):
    is_update_view = True
    template_name = "invoice/invoice_form.html"
    model = Invoice
    form_class = InvoiceForm
    formset_class = InvoiceDetailFormSet


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy("index")
