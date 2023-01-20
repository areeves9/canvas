from django.contrib import admin
from strains.models import Strain, Flavor


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


class FlavorModelAdmin(admin.ModelAdmin):
    """Manage Flavor model in admin."""

    list_display = ["name"]
    list_display_links = ["name"]
    list_filter = ["name"]

    class Meta:
        """Order by flavor."""

        model = Flavor


admin.site.register(Strain, StrainModelAdmin)
admin.site.register(Flavor, FlavorModelAdmin)
