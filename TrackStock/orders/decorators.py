from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


def manager_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "manager":
            messages.error(request, "You do not have permission to access this page or to do this action.")
            return redirect(request.META.get("HTTP_REFERER", reverse("orders:order_list")))
        return view_func(request, *args, **kwargs)

    return _wrapped_view
