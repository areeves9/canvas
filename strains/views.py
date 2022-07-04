import os
from common.decorators import ajax_required

from email.mime.image import MIMEImage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404


from django.views.generic import ListView
from django.views.generic.detail import DetailView


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMultiAlternatives

from reviews.models import Strain, Review
from actions.models import create_action

from reviews.forms import (
    ShareReviewForm,
)


# Create your views here.
@method_decorator(login_required, name="dispatch")
class StrainDetailView(DetailView):
    """Return a strain instance by id."""

    model = Strain
    context_object_name = "strain"
    template_name = "strains/strain_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StrainDetailView, self).get_context_data(**kwargs)
        context["reviews"] = self.get_object().user_review.all()
        context["countries"] = self.get_object().lineage
        context["genetics"] = self.get_object().genetics

        return context


@method_decorator(login_required, name="dispatch")
class StrainListView(ListView):
    """Return a paginated list of strain instances."""

    paginate_by = 16
    template_name = "strains/strains.html"

    def get_queryset(self):
        """Return a queryset of Review objects desc by timestamp."""
        queryset = Strain.objects.all().order_by("name")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StrainListView, self).get_context_data(**kwargs)
        list_strain = Strain.objects.all().order_by("name")
        paginator = Paginator(list_strain, self.paginate_by)

        page = self.request.GET.get("page")

        try:
            strains = paginator.page(page)
        except PageNotAnInteger:
            strains = paginator.page(1)
        except EmptyPage:
            strains = paginator.page(paginator.num_pages)

        context["strains"] = strains
        return context


@method_decorator(login_required, name="dispatch")
class StrainReviewsListView(ListView):
    """Retrun paginated list of reviews associated with a strain instance."""

    paginate_by = 8
    context_object_name = "reviews"
    template_name = "reviews/reviews.html"

    def get_queryset(self, id):
        """Return a queryset of Review objects desc by timestamp."""
        queryset = Review.objects.filter(strain__id=id).all().order_by("-timestamp")
        return queryset

    def get_context_data(self, id, **kwargs):
        """Override context dictionary."""
        context = super(StrainReviewsListView, self).get_context_data(**kwargs)
        context["strain"] = context["reviews"].first().strain
        return context

    def get(self, request, id=None, *args, **kwargs):
        """Extend ListView.get()"""
        self.object_list = self.get_queryset(id=id)
        context = self.get_context_data(id=id)

        if request.is_ajax():
            return render(request, "partials/review_card.html", context)
        return render(request, self.template_name, context)


@login_required
def strain_share(request, id=None):
    """Share a strain instance through email."""
    strain = get_object_or_404(Strain, id=id)
    sent = False
    if request.method == "POST":
        form = ShareReviewForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            cd = form.cleaned_data
            strain_url = request.build_absolute_uri(strain.get_absolute_url())
            subject = "{} ({}) recommends you try {}".format(
                request.user, request.user.email, strain.name
            )
            text_content = 'Read "{}" at {}.'.format(strain.name, strain_url)
            html_content = render_to_string(
                "reviews/share_strain_email.html",
                context={
                    "cd": cd,
                    "strain": strain,
                    "user": request.user,
                    "strain_url": strain_url,
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
            if strain.photo:
                msg_img = MIMEImage(strain.photo_url.read())
                msg_img.add_header("Content-ID", "<{}>".format(strain.photo_url))
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


@login_required
@require_POST
def strain_like(request):
    strain_id = request.POST.get("id")
    action = request.POST.get("action")
    if strain_id and action:
        try:
            strain = Strain.objects.get(id=strain_id)
            if action == "like":
                strain.users_like.add(request.user)
                create_action(request.user, "likes", strain)
            else:
                strain.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except:
            pass
    return JsonResponse({"status": "ko"})
