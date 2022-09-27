from django import forms
from django.forms.models import inlineformset_factory
from django.forms.widgets import Select

from .models import Detail, Invoice, InvoiceDetail, Item


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ("customer",)

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)

        customer_number = [("", "-- テーブル名 --")] + [(str(i), str(i)) for i in range(1, 7)]
        self.fields["customer"].widget = Select(choices=customer_number)


class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = (
            "item",
			"detail",
            "quantity",
        )

    def __init__(self, *args, **kwargs):
        super(InvoiceDetailForm, self).__init__(*args, **kwargs)

        self.fields["item"].choices = lambda: [("", "-- 商品 --")] + [
            (item.id, "%s %s円" % (item.name.ljust(10, "　"), item.unit_price))
            for item in Item.objects.order_by("order")
        ]

        self.fields["detail"].choices = lambda: [("", "-- 詳細 --")] + [
            (detail.id, "%s" % (detail.name.ljust(10)))
            for detail in Detail.objects.order_by("order")
        ]

        choices_number = [("", "-- 個数 --")] + [(str(i), str(i)) for i in range(1, 10)]
        self.fields["quantity"].widget = Select(choices=choices_number)


InvoiceDetailFormSet = inlineformset_factory(
    parent_model=Invoice,
    model=InvoiceDetail,
    form=InvoiceDetailForm,
    extra=1,
    min_num=1,
    validate_min=True,
)
