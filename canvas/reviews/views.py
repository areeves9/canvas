from django.shortcuts import render

from reviews.models import Strain, Review
# Create your views here.

def reviews(request):
    reviews = Review.objects.all()
    context = {
        "reviews": reviews,
    }
    return render(request, "reviews/reviews.html", context)

def strains(request):
    strains = Strain.objects.all()
    context = {
        "strains": strains,
    }
    return render(request, "reviews/strains.html", context)
