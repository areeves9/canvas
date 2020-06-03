from django.urls import re_path
from django.views.generic import TemplateView


from . import views

app_name = 'reviews'

urlpatterns = [
    re_path(r'^$', views.reviews, name="reviews"),
    re_path(r'^(?P<id>\d+)/$', views.review_detail, name="review_detail"),
    re_path(r'^strain/(?P<id>\d+)/$', views.strain_reviews, name="strain_reviews"),
    re_path(r'^(?P<id>\d+)/update/$', views.review_update, name="review_update"),
    re_path(r'^(?P<id>\d+)/delete/$', views.review_delete, name="review_delete"),
    re_path(r'^(?P<id>\d+)/share/$', views.review_share, name="share_review"),
    re_path(r'^review-like/$', views.review_like, name="review_like"),
    re_path(r'^strains/$', views.strains, name="strains"),
    re_path(r'^strains/(?P<id>\d+)/$', views.strain_detail, name="strain_detail"),
    re_path(r'^strains/(?P<id>\d+)/review/$', views.strain_review, name="strain_review"),
    re_path(r'^strain-like/$', views.strain_like, name="strain_like"),
    re_path(r'^strains/(?P<id>\d+)/share/$', views.strain_share, name="share_strain"),
    re_path(r'^reviews-search/$', TemplateView.as_view(template_name='reviews/reviews_search.html'), name='reviews_search'),
]
