from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.reviews, name="reviews"),
    url(r'^(?P<id>\d+)/$', views.review_detail, name="detail"),
    url(r'^(?P<id>\d+)/update/$', views.review_update, name="update"),
    url(r'^like/$', views.review_like, name="like"),
    url(r'^strains/$', views.strains, name="strains"),
    url(r'^strains/(?P<id>\d+)/$', views.strain_detail, name="strain"),
    url(r'^strains/(?P<id>\d+)/review/$', views.strain_review, name="review"),
]
