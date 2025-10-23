from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    # /accounts/signup/  -> your signup view (accounts.views.signup)
    path('signup/', views.signup, name='signup'),

    # custom function-based login view that redirects to dashboard
    path('login/', views.login_view, name='login'),

    # Include the rest of Django's built-in auth views (logout, password reset, etc.)
    path('', include('django.contrib.auth.urls')),
]