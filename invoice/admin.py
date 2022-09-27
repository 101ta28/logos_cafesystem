from django.contrib import admin

from .models import Detail, Invoice, InvoiceDetail, Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "unit_price",
        "order",
    )
    list_editable = (
        "unit_price",
        "order",
    )
    ordering = ("order",)


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "order",
    )
    list_editable = ("order",)
    ordering = ("order",)


class InvoiceDetailInline(admin.TabularInline):
    model = InvoiceDetail
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceDetailInline]
