import os
from common.decorators import ajax_required

from email.mime.image import MIMEImage
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404


from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView


from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string


from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives

from reviews.models import Strain, Review
from actions.models import create_action

from reviews.forms import (
    ReviewForm,
    CommentForm,
    ShareReviewForm,
)


# Create your views here.
@method_decorator(login_required, name="dispatch")
class ReviewListView(ListView):
    """Return a paginated list of review instances."""

    paginate_by = 8
    model = Review
    context_object_name = "reviews"
    template_name = "reviews/reviews.html"

    def get_queryset(self):
        """Return a queryset of Review objects descending by timestamp."""
        queryset = Review.objects.all().order_by("-timestamp")
        return queryset

    def get_context_data(self, **kwargs):
        """Override context dictioanry."""
        context = super(ReviewListView, self).get_context_data(**kwargs)
        context["nav"] = "home"
        return context

    def get(self, request, *args, **kwargs):
        """Extend ListView.get()"""
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        if request.is_ajax():
            return render(request, "partials/reviews/review_card.html", context)
        return render(request, self.template_name, context)


# returns a Review instance
@method_decorator(login_required, name="dispatch")
class ReviewDetailView(DetailView):
    """Return a strain instance by id."""

    model = Review
    form_class = CommentForm
    template_name = "reviews/review_detail.html"


@method_decorator(login_required, name="dispatch")
class ReviewUpdateView(UpdateView):
    """Update a review instance."""

    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        """Override is_valid method and return form instance."""
        if form.is_valid():
            review = form.save()
            flavors = form.cleaned_data["flavors"]
            review.save()
            review.flavors.set(flavors)
            create_action(self.request.user, "updated", review)
            messages.success(self.request, "Updated review {}".format(review))
            return super(ReviewUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, "Review failed to save.")


@method_decorator(login_required, name="dispatch")
class ReviewStrain(CreateView, SuccessMessageMixin):
    """Create a Strain instance."""

    model = Review
    form_class = ReviewForm
    template_name = "reviews/review_form.html"
    success_message = "Review saved."

    def form_valid(self, form):
        """Override is_valid method and return form instance."""
        if form.is_valid():
            review = form.save()
            flavors = form.cleaned_data["flavors"]
            user = self.request.user
            review.strain = get_object_or_404(Strain, id=self.kwargs.get("pk"))
            review.user = user
            review.save()
            review.flavors.set(flavors)
            create_action(self.request.user, "wrote", review)
            return super(ReviewStrain, self).form_valid(form)
        else:
            messages.error(self.request, "Review failed to save.")
            return self.form_class()

    def get_success_url(self):
        """Return the review list view."""
        return reverse("reviews:reviews")


# @login_required
# def review_detail(request, id=None):
#     review = get_object_or_404(Review, id=id)
#     comments = review.comments.filter(active=True)
#     comment_form = CommentForm(request.POST or None)
#     if comment_form.is_valid():
#         new_comment = comment_form.save(commit=False)
#         new_comment.review = review
#         new_comment.user = request.user
#         new_comment.save()
#         create_action(request.user, "commented on", review)
#         messages.success(request, "Comment posted.")
#         return HttpResponseRedirect(review.get_absolute_url())
#     else:
#         context = {
#             "review": review,
#             "comments": comments,
#             "comment_form": comment_form,
#         }
#     return render(request, "reviews/review_detail.html", context)


@login_required
def review_delete(request, id=None):
    """Delete a review instance."""
    review = get_object_or_404(Review, id=id)
    if review.user != request.user:
        raise PermissionDenied
    elif review.user == request.user:
        review.delete()
        create_action(request.user, "deleted", review)
        messages.success(request, "Deleted review.")
        return HttpResponseRedirect(reverse("reviews:reviews"))


@login_required
@require_POST
def review_like(request):
    """User association to a post."""
    review_id = request.POST.get("id")
    action = request.POST.get("action")
    if review_id and action:
        try:
            review = Review.objects.get(id=review_id)
            if action == "like":
                review.users_like.add(request.user)
                create_action(request.user, "likes", review)
            else:
                review.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Review.DoesNotExist:
            pass
    return JsonResponse({"status": "ko"})


@login_required
def review_share(request, id=None):
    """Share a review instance through email."""
    review = get_object_or_404(Review, id=id)
    sent = False
    if request.method == "POST":
        form = ShareReviewForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            cd = form.cleaned_data
            review_url = request.build_absolute_uri(review.get_absolute_url())
            subject = "{} ({}) recommends you reading {}".format(
                request.user, request.user.email, review.title
            )
            text_content = 'Read "{}" at {}.'.format(review.title, review_url)
            html_content = render_to_string(
                "reviews/share_review_email.html",
                context={
                    "cd": cd,
                    "review": review,
                    "user": request.user,
                    "review_url": review_url,
                },
            )
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                os.environ["CANVAS_DEFAULT_FROM_EMAIL"],
                [cd["send_to"]],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.mixed_subtype = "related"
            if review.photo:
                msg_img = MIMEImage(review.photo.read())
                msg_img.add_header("Content-ID", "<{}>".format(review.photo))
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
