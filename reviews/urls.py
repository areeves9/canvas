from django.urls import path
from django.views.generic import TemplateView


from . import views
from reviews.views import (
    ReviewDetailView,
    ReviewListView,
    ReviewUpdateView,
    ReviewStrain,
)

app_name = "reviews"

urlpatterns = [
    path("", ReviewListView.as_view(), name="reviews"),
    path("<pk>", ReviewDetailView.as_view(), name="review_detail"),
    path("<pk>/update", ReviewUpdateView.as_view(), name="review_update"),
    path("<id>/delete", views.review_delete, name="review_delete"),
    path("<id>/share", views.review_share, name="share_review"),
    path("like/review", views.review_like, name="review_like"),
    # replace this with a query param to filter reviews by strain
    path("strains/<pk>/review", ReviewStrain.as_view(), name="strain_review"),
    path(
        "search/",
        TemplateView.as_view(template_name="reviews/reviews_search.html"),
        name="reviews_search",
    ),
]
