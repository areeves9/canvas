from django.contrib import admin

from reviews.models import Review, Strain
# Register your models here.

class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "strain", "rating", "timestamp"]
    list_display_links = ["title"]
    list_filter = ["strain"]
    class Meta:
        model = Review

class StrainModelAdmin(admin.ModelAdmin):
    list_display = ["name", "genetics", "lineage"]
    list_display_links = ["name"]


admin.site.register(Review, ReviewModelAdmin)
admin.site.register(Strain, StrainModelAdmin)
