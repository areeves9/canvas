from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from reviews.forms import ReviewForm
from reviews.models import Strain, Review
# Create your views here.

def reviews(request):
    reviews = Review.objects.all()
    context = {
        "reviews": reviews,
    }
    return render(request, "reviews/reviews.html", context)

def review_detail(request, id=None):
    review = get_object_or_404(Review, id=id)
    context = {
        "review": review,
    }
    return render(request, "reviews/review_detail.html", context)

def strains(request):
    strains = Strain.objects.all()
    context = {
        "strains": strains,
    }
    return render(request, "reviews/strains.html", context)

def strain_detail(request, id=None):
    strain = get_object_or_404(Strain, id=id)
    context = {
        "strain": strain,
    }
    return render(request, "reviews/strain_detail.html", context)

@login_required
def strain_review(request, id=None):
    strain = get_object_or_404(Strain, id=id)
    form = ReviewForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        method = form.cleaned_data['method']
        photo = form.cleaned_data['photo']
        user = request.user
        review = Review()
        review.strain = strain
        review.user = user
        review.title = title
        review.content = content
        review.method = method
        review.photo = photo
        review.save()
        return HttpResponseRedirect(review.get_absolute_url())
    else:
        pass
    context = {
        "form": form,
        "strain": strain,
    }
    return render(request, "reviews/review_form.html", context)
