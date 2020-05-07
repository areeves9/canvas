from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^reviews/$', views.reviews, name="reviews"),
    url(r'^reviews/(?P<id>\d+)/$', views.reviews_strain, name="reviews_strain"),
    url(r'^(?P<id>\d+)/$', views.review_detail, name="detail"),
    url(r'^(?P<id>\d+)/update/$', views.review_update, name="update"),
    url(r'^(?P<id>\d+)/delete/$', views.review_delete, name="delete"),
    url(r'^(?P<id>\d+)/share/$', views.review_share, name="share"),
    url(r'^like/$', views.review_like, name="like"),
    url(r'^strain-like/$', views.strain_like, name="strain_like"),
    url(r'^strains/$', views.strains, name="strains"),
    url(r'^strains/$', views.strains, name="strains"),
    url(r'^(?P<id>\d+)/share/strain/$', views.strain_share, name="share_strain"),
    url(r'^strains/(?P<id>\d+)/$', views.strain_detail, name="strain"),
    url(r'^strains/(?P<id>\d+)/review/$', views.strain_review, name="review"),
]
