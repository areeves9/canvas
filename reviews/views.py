from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from reviews.forms import ReviewForm, CommentForm
from reviews.models import Strain, Review, Comment

from actions.models import Action, create_action

from django.views.decorators.http import require_POST
from common.decorators import ajax_required


import json
# Create your views here.
def reviews(request):
    review_list = Review.objects.all().order_by("-timestamp")
    paginator = Paginator(review_list, 8)
    page = request.GET.get('page')
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        reviews = paginator.page(paginator.num_pages)
    if request.is_ajax():
        context = {
            "reviews": reviews,
        }
        return render(request, "reviews/review_list_ajax.html", context)
    context = {
        "reviews": reviews,
    }
    return render(request, "reviews/reviews.html", context)

@login_required
def review_detail(request, id=None):
    review = get_object_or_404(Review, id=id)
    comments = review.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.review = review
            new_comment.name = request.user.username
            new_comment.email = request.user.email
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        "review": review,
        "comments": comments,
        "comment_form": comment_form,
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
                create_action(request.user, 'likes', review)
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
    strain_list = Strain.objects.all().order_by("name")
    paginator = Paginator(strain_list, 8)
    page = request.GET.get('page')
    try:
        strains = paginator.page(page)
    except PageNotAnInteger:
        strains = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        strains = paginator.page(paginator.num_pages)
    if request.is_ajax():
        context = {
            "strains": strains,
        }
        return render(request, "reviews/strain_list_ajax.html", context)
    context = {
        "strains": strains,
    }
    return render(request, "reviews/strains.html", context)

def strain_detail(request, id=None):
    strain = get_object_or_404(Strain, id=id)
    reviews = strain.user_review.all()
    countries = strain.lineage
    genetics = strain.genetics
    context = {
        "strain": strain,
        "reviews": reviews,
        "countries": countries,
        "genetics": genetics,
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
        rating = form.cleaned_data['rating']
        user = request.user
        review = Review()
        review.strain = strain
        review.user = user
        review.title = title
        review.content = content
        review.method = method
        review.photo = photo
        review.rating = rating
        review.save()
        create_action(request.user, 'wrote review', review.title)
        messages.success(request, "Review saved.")
        return HttpResponseRedirect(review.get_absolute_url())
    else:
        messages.error(request, "Review failed to save.")
    context = {
        "form": form,
        "strain": strain,
    }
    return render(request, "reviews/review_form.html", context)
