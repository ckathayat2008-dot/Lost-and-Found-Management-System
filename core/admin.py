
from django.contrib import admin
from .models import Item


@admin.action(description="Mark selected items as Claimed")
def mark_claimed(modeladmin, request, queryset):
    queryset.update(status='Claimed')


@admin.action(description="Mark selected items as Returned")
def mark_returned(modeladmin, request, queryset):
    queryset.update(status='Returned')


@admin.action(description="Mark selected items as Active")
def mark_active(modeladmin, request, queryset):
    queryset.update(status='Active')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'item_name',
        'item_type',
        'category',
        'location',
        'date_lost_found',
        'status',
        'reported_by',
    )

    list_filter = (
        'item_type',
        'category',
        'status',
        'date_lost_found',
    )

    search_fields = (
        'item_name',
        'description',
        'location',
    )

    ordering = ('-created_at',)

    actions = [
        mark_claimed,
        mark_returned,
        mark_active,
    ]
