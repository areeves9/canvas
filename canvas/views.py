from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('reviews:reviews'))
    else:
        return login(request)
