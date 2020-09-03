from django.contrib import admin
from .models import Search

class SearchAdmin(admin.ModelAdmin):
    fieldsets = [
        ("search", {"fields": ["search"]}),
        ("search date", {"fields": ["search_date"]}),
        ("slug", {"fields": ["slug"]}),
    ]

admin.site.register(Search, SearchAdmin)
