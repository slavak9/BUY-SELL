from django.shortcuts import render, redirect

def csrf_failure(request, reason=""):
    """Default view for CSRF failures."""
    if str(request)[0:30] == "<WSGIRequest: POST '/accounts/" and request.user.is_authenticated:
       return redirect(request.GET['next'])
    return render(
        request,
        "main_app/csrf_forbidden.html",
        {"reason": 'polklksfd'},
        status=403,
    )
