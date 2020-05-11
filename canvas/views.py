from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('reviews:reviews'))
    return render(request, 'index.html')
