from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect


def user_role_required(*oargs):
    """Decorator to restrict view access based on the user's role."""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            role_satisfied = False
            for oarg in oargs:
                try:
                    if request.user.usertype == oarg:
                        role_satisfied = True
                        break
                except AttributeError:
                    return redirect("main:login")
            if request.user.is_authenticated and role_satisfied:
                # Allow access if the user has the required role
                return view_func(request, *args, **kwargs)
            else:
                # Deny access if the user does not have the required role
                raise PermissionDenied  # or redirect to a different page

        return _wrapped_view

    return decorator
