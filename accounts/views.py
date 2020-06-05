from common.decorators import ajax_required

from django.http import Http404, JsonResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import CreateView
from django.views.decorators.http import require_POST


from accounts.models import Follow
from accounts.forms import ProfileForm, UserForm, UserRegisterForm

from reviews.models import Review
from actions.models import Action, create_action
# Create your views here.


class RegistrationView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('reviews:reviews')

    def form_valid(self, form):
        valid = super(RegistrationView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Follow.objects.get_or_create(follow_from=request.user, follow_to=user)
                create_action(request.user, 'is following', user)
            else:
                Follow.objects.filter(follow_from=request.user, follow_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
        return JsonResponse({'status': 'ko'})


@login_required
def profile(request):
    user = request.user
    review_list = Review.objects.filter(user=user)
    review_numbers = Review.objects.filter(user=user).count()
    followers = user.followers.all()
    following = user.following.all()
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions[:10]
    context = {
        "user": user,
        "review_list": review_list,
        "review_numbers": review_numbers,
        "followers": followers,
        "following": following,
        "actions": actions,
        "nav": 'profile',
    }
    return render(request, "accounts/profile.html", context)


@login_required
def profile_user(request, username=""):
    if username:
        try:
            user = User.objects.get(username=username)
            review_list = Review.objects.filter(user=user)
            review_numbers = Review.objects.filter(user=user).count()
            followers = user.followers.all()
            following = user.following.all()
        except User.DoesNotExist:
            raise Http404
        context = {
            "user": user,
            "review_list": review_list,
            "review_numbers": review_numbers,
            "followers": followers,
            "following": following,
            "nav": 'profile',
        }
        return render(request, "accounts/profile.html", context)


@login_required
def profile_update(request):
    if request.method == "POST":
        user_form = UserForm(request.POST or None, instance=request.user)
        profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            user.save()
            profile.save()
            messages.success(request, "Profile updated successfully.")
            return redirect(reverse("accounts:profile"))
        else:
            messages.error(request, "Please correct the fields below.")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "accounts/profile_update.html", context)


@login_required
def actions(request):
    actions = Action.objects.filter(user=request.user)
    actions = actions[:10]
    context = {
        'actions': actions,
        'nav': 'actions',
    }
    return render(request, "actions/actions.html", context)
