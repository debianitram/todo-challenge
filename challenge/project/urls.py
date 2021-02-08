from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import RedirectView

from .router import router

admin.site.site_header = getattr(settings, 'PROJECT_NAME_HEADER')
admin.site.site_title = getattr(settings, 'PROJECT_NAME_TITLE')

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
