from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import Shipment


def order_status_required(status="Pending"):

    def decorator(view_func):
        def _wrapped_view(request, shipment_id, *args, **kwargs):
            shipment = get_object_or_404(Shipment, id=shipment_id)

            if shipment.status != status:
                messages.error(request, f"Action not allowed! Order must be '{status}', but it's '{shipment.status}'.")
                return redirect(request.META.get("HTTP_REFERER", reverse("shipment:shipment_list")))

            return view_func(request, shipment_id, *args, **kwargs)

        return _wrapped_view

    return decorator


def manager_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "manager":
            messages.error(request, "You do not have permission to access this page or to do this action.")
            return redirect(request.META.get("HTTP_REFERER", reverse("shipment:shipment_list")))
        return view_func(request, *args, **kwargs)

    return _wrapped_view