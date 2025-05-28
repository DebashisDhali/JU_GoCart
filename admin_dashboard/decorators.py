# admin_dashboard/decorators.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def admin_login_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_authenticated and user.is_staff,
        login_url='admin_login'
    )(view_func)
    return decorated_view_func