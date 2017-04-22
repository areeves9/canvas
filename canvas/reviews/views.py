from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse

from reviews.forms import ReviewForm
from reviews.models import Strain, Review

from django.views.decorators.http import require_POST

import json
# Create your views here.

def reviews(request):
    review_list = Review.objects.all().order_by("-timestamp")
    paginator = Paginator(review_list, 10)
    page = request.GET.get('page')
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
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

@login_required
@require_POST
def review_like(request):
    review_id = request.POST.get('id')
    action = request.POST.get('action')
    if review_id and action:
        try:
            review = Review.objects.get(id=review_id)
            if action == 'like':
                review.users_like.add(request.user)
            else:
                review.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})

@login_required
def review_update(request, id=None):
    review = get_object_or_404(Review, id=id)
    if review.user == request.user:
        form = ReviewForm(request.POST or None, request.FILES or None, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            messages.success(request, "<a href=''>Item</a> Saved", extra_tags="html_safe")
            return HttpResponseRedirect( '/reviews/')
        else:
            messages.error(request, "Update failed.")
        context = {
            "form": form,
            "review": review,
        }
        return render(request, "reviews/review_form.html", context)

def strains(request):
    strains = Strain.objects.all()
    context = {
        "strains": strains,
    }
    return render(request, "reviews/strains.html", context)

def strain_detail(request, id=None):
    strain = get_object_or_404(Strain, id=id)
    countries = strain.lineage
    context = {
        "strain": strain,
        "countries": countries,
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
        messages.success(request, "Review saved.")
        return HttpResponseRedirect(review.get_absolute_url())
    else:
        messages.error(request, "Review failed to save.")
    context = {
        "form": form,
        "strain": strain,
    }
    return render(request, "reviews/review_form.html", context)
