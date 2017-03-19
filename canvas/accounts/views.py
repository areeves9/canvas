from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from accounts.models import Profile
from accounts.forms import ProfileForm, UserForm
# Create your views here.
@login_required
def profile(request):
    user = request.user
    context = {
        "user": user,
    }
    return render(request, "accounts/profile.html", context)

@login_required
def profile_update(request):
    if request.method == "POST":
        user_form = UserForm(request.POST or None, instance=request.user)
        profile_form = ProfileForm(request.POST or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            user.save()
            profile.save()
            return redirect("profile")
        else:
            pass
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "accounts/profile_form.html", context)
