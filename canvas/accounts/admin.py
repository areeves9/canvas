from django.contrib import admin

# Register your models here.
from accounts.models import Profile

class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ["user", "location", "birthdate"]
    list_display_link = ["user"]
    class Meta:
        model = Profile

admin.site.register(Profile, ProfileModelAdmin)
