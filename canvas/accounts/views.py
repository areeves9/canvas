from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404

from accounts.models import Profile
from accounts.forms import ProfileForm, UserForm

from reviews.models import Review
# Create your views here.
def users(request):
    users = User.objects.all()
    context = {
        "users": users,
    }
    return render(request, "accounts/users.html", context)


@login_required
def profile(request):
    user = request.user
    review_list = Review.objects.filter(user=user)
    review_numbers = Review.objects.filter(user=user).count()
    context = {
        "user": user,
        "review_list": review_list,
        "review_numbers": review_numbers,
    }
    return render(request, "accounts/profile.html", context)

@login_required
def profile_user(request, username=""):
    if username:
        try:
            user = User.objects.get(username=username)
            review_list = Review.objects.filter(user=user)
            review_numbers = Review.objects.filter(user=user).count()
        except User.DoesNotExist:
            raise Http404
        context = {
            "user": user,
            "review_list": review_list,
            "review_numbers": review_numbers,
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
            return redirect("accounts:profile")
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
