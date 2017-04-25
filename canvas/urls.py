"""canvas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from canvas.settings import base


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^reviews/', include('reviews.urls', namespace='reviews')),
]

if base.DEBUG:
    urlpatterns += static(base.STATIC_URL, document_root=base.STATIC_ROOT)
    urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)
