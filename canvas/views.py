from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.views import login
from django.contrib.auth.decorators import user_passes_test


# def index(request):
#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('reviews:reviews'))
#     else:
#         return render(request, 'index.html')
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('reviews:reviews'))
    else:
        return login(request)
