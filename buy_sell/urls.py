"""buy_sell URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from main_app.views import HandlerError403

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if not settings.DEBUG:
    urlpatterns.append(re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}))
    urlpatterns.append(re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}))


handler403 = HandlerError403.as_view()


# make auto update
def update_migrations():
    from django.core.management import call_command
    call_command('makemigrations')
    call_command('migrate')
    print('UPDATE MIGRATIONS WAS MADE FROM BUY_SELL URLS.PY')
update_migrations()