from django.urls import path
from django.views.generic import TemplateView


from . import views
from reviews.views import ReviewListView

app_name = "reviews"

urlpatterns = [
    path("", ReviewListView.as_view(), name="reviews"),
    # path("", views.reviews, name="review_detail"),
    path("<id>", views.review_detail, name="review_detail"),
    # replace this with a query param to filter reviews by strain
    path("strain/<id>", views.strain_reviews, name="strain_reviews"),
    path("<id>/update", views.review_update, name="review_update"),
    path("<id>/delete", views.review_delete, name="review_delete"),
    path("<id>/share", views.review_share, name="share_review"),
    path("like/review", views.review_like, name="review_like"),
    path("strains/list", views.strains, name="strains"),
    path("strains/<id>", views.strain_detail, name="strain_detail"),
    path("strains/<id>/review", views.strain_review, name="strain_review"),
    path("like/strain", views.strain_like, name="strain_like"),
    path("strains/<id>/share", views.strain_share, name="share_strain"),
    path(
        "search/",
        TemplateView.as_view(template_name="reviews/reviews_search.html"),
        name="reviews_search",
    ),
]
