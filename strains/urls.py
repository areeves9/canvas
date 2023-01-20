from django.urls import path
from django.views.generic import TemplateView


from . import views
from strains.views import (
    StrainListView,
    StrainReviewsListView,
    StrainDetailView,
)

app_name = "strains"

urlpatterns = [
    path("strain/<id>", StrainReviewsListView.as_view(), name="strain_reviews"),
    path("strains/", StrainListView.as_view(), name="strains"),
    path("strains/<pk>/", StrainDetailView.as_view(), name="strain_detail"),
    path("strains/<id>/share", views.strain_share, name="share_strain"),
    path("like/strain", views.strain_like, name="strain_like"),
]
