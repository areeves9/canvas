from django.contrib import admin
from reviews.models import Strain


# Register your models here.
class StrainModelAdmin(admin.ModelAdmin):
    """Manage strain model in admin."""

    list_display = ["name", "ocpc", "lineage", "created_at"]
    list_display_links = ["name"]
    search_fields = ["name"]

    class Meta:
        """Order instances by name."""

        model = Strain
        ordering = ["-name"]


admin.site.register(Strain, StrainModelAdmin)
