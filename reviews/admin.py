from django.contrib import admin

from reviews.models import Review, Strain, Comment, Flavor

# Register your models here.


class ReviewModelAdmin(admin.ModelAdmin):
    """Review model for admin."""

    list_display = [
        "title",
        "user",
        "strain",
        "rating",
        "timestamp",
        "photo",
        "get_flavors",
    ]
    list_display_links = ["title"]
    list_filter = ["strain", "user", "rating"]

    class Meta:
        model = Review


# class CommentModelAdmin(admin.ModelAdmin):
#     list_display = ["user", "review", "created", "active"]
#     list_filter = ["active", "created", "updated"]
#     search_fields = ["user", "body"]

#     class Meta:
#         model = Comment


admin.site.register(Review, ReviewModelAdmin)
