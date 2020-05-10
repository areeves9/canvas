from django.conf.urls import url
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    # all reviews
    url(r'^$', views.reviews, name="reviews"),
    # review instance
    url(r'^(?P<id>\d+)/$', views.review_detail, name="review_detail"),
    url(r'^strain/(?P<id>\d+)/$', views.strain_reviews, name="strain_reviews"),
    url(r'^(?P<id>\d+)/update/$', views.review_update, name="review_update"),
    url(r'^(?P<id>\d+)/delete/$', views.review_delete, name="review_delete"),
    url(r'^(?P<id>\d+)/share/$', views.review_share, name="share_review"),
    url(r'^review-like/$', views.review_like, name="review_like"),
    url(r'^strains/$', views.strains, name="strains"),
    # reviews filtered by strain id
    url(r'^strains/(?P<id>\d+)/$', views.strain_detail, name="strain_detail"),
    url(r'^strains/(?P<id>\d+)/review/$', views.strain_review, name="strain_review"),
    url(r'^strain-like/$', views.strain_like, name="strain_like"),
    url(r'^strains/(?P<id>\d+)/share/$', views.strain_share, name="share_strain"),
    url(r'^search/$', TemplateView.as_view(template_name='reviews/reviews_search.html'), name='reviews_search'),
]
