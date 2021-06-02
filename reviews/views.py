import os
from common.decorators import ajax_required

from email.mime.image import MIMEImage
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse
)
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string

from django.urls import reverse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives

from reviews.forms import ReviewForm, CommentForm, ShareReviewForm
from reviews.models import Strain, Review
from actions.models import create_action


# Create your views here.
@login_required
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
        return render(request, "partials/review_card.html", context)
    context = {
        "reviews": reviews,
        "nav": 'home',
    }
    return render(request, "reviews/reviews.html", context)


# returns a query set of reviews filtered by strain id
@login_required
def strain_reviews(request, id=None):
    review_list = Review.objects.filter(strain__id=id).all().order_by("-timestamp")
    strain = review_list.first().strain
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
        return render(request, "partials/review_card.html", context)
    context = {
        "reviews": reviews,
        "strain": strain,
    }
    return render(request, "reviews/reviews.html", context)


# returns a Review instance
@login_required
def review_detail(request, id=None):
    review = get_object_or_404(Review, id=id)
    comments = review.comments.filter(active=True)
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.review = review
        new_comment.user = request.user
        new_comment.save()
        create_action(request.user, 'commented on', review)
        messages.success(request, "Comment posted.")
        return HttpResponseRedirect(review.get_absolute_url())
    else:
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
@require_POST
def strain_like(request):
    strain_id = request.POST.get('id')
    action = request.POST.get('action')
    if strain_id and action:
        try:
            strain = Strain.objects.get(id=strain_id)
            if action == 'like':
                strain.users_like.add(request.user)
                create_action(request.user, 'likes', strain)
            else:
                strain.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required
def review_update(request, id=None):
    review = get_object_or_404(Review, id=id)
    if review.user != request.user:
        raise PermissionDenied
    elif review.user == request.user:
        form = ReviewForm(
            request.POST or None,
            request.FILES or None,
            instance=review
        )
        if form.is_valid():
            review = form.save()
            review.save()
            create_action(request.user, 'updated', review)
            messages.success(request, "Updated review {}".format(review))
            return HttpResponseRedirect(reverse('reviews:reviews'))
        context = {
            "form": form,
            "review": review,
        }
        return render(request, "reviews/review_form.html", context)
        

@login_required
def review_delete(request, id=None):
    review = get_object_or_404(Review, id=id)
    if review.user != request.user:
        raise PermissionDenied
    elif review.user == request.user:
        review.delete()
        create_action(request.user, 'deleted', review)
        messages.success(request, "Deleted review.")
        return HttpResponseRedirect(reverse('reviews:reviews'))


@login_required
def review_share(request, id=None):
    review = get_object_or_404(Review, id=id)
    sent = False
    if request.method == 'POST':
        form = ShareReviewForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            cd = form.cleaned_data
            review_url = request.build_absolute_uri(review.get_absolute_url())
            subject = '{} ({}) recommends you reading {}'.format(
                request.user, request.user.email, review.title
                )
            text_content = 'Read "{}" at {}.'.format(review.title, review_url)
            html_content = render_to_string(
                            'reviews/share_review_email.html',
                            context={
                                'cd': cd,
                                'review': review,
                                'user': request.user,
                                'review_url': review_url,
                                }
                        )
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                os.environ['CANVAS_DEFAULT_FROM_EMAIL'],
                [cd['send_to']]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.mixed_subtype = 'related'
            if review.photo:
                msg_img = MIMEImage(review.photo.read())
                msg_img.add_header('Content-ID', '<{}>'.format(review.photo))
                msg.attach(msg_img)
                msg.send()
            else:
                msg.send()
            messages.success(request, "Message sent")
            return HttpResponseRedirect(review_url)
    else:
        form = ShareReviewForm()
    context = {
        "form": form,
        "review": review,
        "sent": sent,
    }
    return render(request, "partials/share_form.html", context)


@login_required
def strain_share(request, id=None):
    strain = get_object_or_404(Strain, id=id)
    sent = False
    if request.method == 'POST':
        form = ShareReviewForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            cd = form.cleaned_data
            strain_url = request.build_absolute_uri(strain.get_absolute_url())
            subject = '{} ({}) recommends you try {}'.format(
                request.user, request.user.email, strain.name
                )
            text_content = 'Read "{}" at {}.'.format(strain.name, strain_url)
            html_content = render_to_string(
                            'reviews/share_strain_email.html',
                            context={
                                'cd': cd,
                                'strain': strain,
                                'user': request.user,
                                'strain_url': strain_url,
                                }
                        )
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                os.environ['CANVAS_DEFAULT_FROM_EMAIL'],
                [cd['send_to']]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.mixed_subtype = 'related'
            if strain.photo:
                msg_img = MIMEImage(strain.photo_url.read())
                msg_img.add_header('Content-ID', '<{}>'.format(strain.photo_url))
                msg.attach(msg_img)
                msg.send()
            else:
                msg.send()
            messages.success(request, "Strain shared.")
            return HttpResponseRedirect(strain_url)
    else:
        form = ShareReviewForm()
    context = {
        "form": form,
        "strain": strain,
        "sent": sent,
    }
    return render(request, "partials/share_form.html", context)


# get all the strains (paginated) from the db
@login_required
def strains(request):
    strain_list = Strain.objects.all().order_by("name")
    paginator = Paginator(strain_list, 18)
    page = request.GET.get('page')
    try:
        strains = paginator.page(page)
    except PageNotAnInteger:
        strains = paginator.page(1)
    except EmptyPage:
        strains = paginator.page(paginator.num_pages)
    context = {
        "strains": strains,
        "nav": 'strains',
    }
    return render(request, "reviews/strains.html", context)


@login_required
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
    if request.method == 'POST':
        form = ReviewForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            review = Review()
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            method = form.cleaned_data['method']
            photo = form.cleaned_data['photo']
            rating = form.cleaned_data['rating']
            user = request.user
            review.strain = strain
            review.user = user
            review.title = title
            review.content = content
            review.method = method
            review.photo = photo
            review.rating = rating
            review.save()
            create_action(request.user, 'wrote', review)
            messages.success(request, "Review saved.")
            return HttpResponseRedirect(review.get_absolute_url())
        else:
            messages.error(request, "Review failed to save.")

    else:
        form = ReviewForm()
    context = {
        "form": form,
        "strain": strain,
    }
    return render(request, "reviews/review_form.html", context)
