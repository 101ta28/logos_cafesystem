from random import choices

from django.contrib.auth.models import User
from django_filters import FilterSet, filters

from .models import Invoice


class MyOrderingFilter(filters.OrderingFilter):
    descending_fmt = "%s （降順）"


class InvoiceFilter(FilterSet):
    customer = filters.ChoiceFilter(choices=[(str(i), str(i)) for i in range(1, 7)])
    order_by = MyOrderingFilter(
        # tuple-mapping retains order
        fields=(("created_at", "created_at"),),
        field_labels={
            "created_at": "登録時間",
        },
        label="並び順",
    )

    class Meta:
        model = Invoice
        fields = ("customer",)
