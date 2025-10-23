from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # saves User and profile
            messages.success(request, "Account created. Please log in to continue.")
            # Redirect to login page (with optional next param preserved)
            # Prefer next from POST (preserved by a hidden field), then GET, then fallback
            next_url = request.POST.get('next') or request.GET.get('next') or reverse('accounts:login')
            # Validate next_url is safe (prevents open redirects)
            if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                next_url = reverse('accounts:login')
            return redirect(next_url)
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    """Function-based login view: authenticate and redirect to dashboard.

    Accepts GET (render form) and POST (process credentials). Preserves a safe
    `next` parameter when present.
    """
    next_url = request.GET.get('next') or request.POST.get('next') or None

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # validate next
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('core:dashboard')
    else:
        form = AuthenticationForm(request)

    return render(request, 'registration/login.html', {'form': form, 'next': next_url})

