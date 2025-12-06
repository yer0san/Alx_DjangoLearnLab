from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileUpdateForm
from .forms import CustomUserCreationForm


def index(request):
    return render(request, 'blog/base.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {"form" : form})

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'
    def get_success_url(self):
        return '/'


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("home")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "blog/profile.html", {"form": form})

@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return render(request, "blog/logout.html")