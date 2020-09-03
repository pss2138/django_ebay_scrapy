from django.contrib import admin

from .models import Results, Recommendations, Categories, Price, Duration, Related, ShippingCost


class ResultsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("item info", 
        {"fields": ["category", "cat_id", "price", "shippingcost", "starttime", "endtime", "url", "duration"]}),
    ]


class RecommendationsAdmin(admin.ModelAdmin):
    fieldsets = [
          ("recommendations", 
          {"fields": ["keyword", "counts"]}),
    ]


class CategoriesAdmin(admin.ModelAdmin):
    fieldsets = [
          ("categoreis", 
          {"fields": ["category", "percentage"]}),
    ]


class PriceAdmin(admin.ModelAdmin):
    fieldsets = [
          ("price", 
          {"fields": ["percentage", "price"]}),
    ]


class ShippingCostAdmin(admin.ModelAdmin):
    fieldsets = [
          ("shipping cost", 
          {"fields": ["cost", "counts"]}),
    ]


class DurationAdmin(admin.ModelAdmin):
    fieldsets = [
          ("duration", 
          {"fields": ["percentage", "duration"]}),
    ]

    
class RelatedAdmin(admin.ModelAdmin):
    fieldsets = [
          ("item info", 
          {"fields": ["category", "price", "shippingcost", "url", "watchcount"]}),
    ]


admin.site.register(Results, ResultsAdmin)
admin.site.register(Recommendations, RecommendationsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Duration, DurationAdmin)
admin.site.register(Related, RelatedAdmin)
