from django.contrib import admin

from contact import models


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = 'id', 'category', 'first_name', 'last_name', 'phone', 'email', 'created_date', # noqa
    ordering = '-id',
    # list_filter = 'created_date',
    search_fields = 'id', 'first_name', 'last_name', 'phone',
    list_per_page = 10
    list_max_show_all = 200
    list_display_links = 'id', 'first_name'


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    ordering = '-id',
