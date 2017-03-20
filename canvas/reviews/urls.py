from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.reviews, name="reviews"),
    url(r'^(?P<id>\d+)/$', views.review_detail, name="detail"),
    url(r'^strains$', views.strains, name="strains")
]
