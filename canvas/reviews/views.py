from django.shortcuts import render

from reviews.models import Strain
# Create your views here.
def strains(request):
    strains = Strain.objects.all()
    context = {
        "strains": strains,
    }
    return render(request, "reviews/strains.html", context)
