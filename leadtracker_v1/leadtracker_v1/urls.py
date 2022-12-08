"""leadtracker_v1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, register_converter
from django.conf.urls import url
from django.conf.urls import include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from common.drf_custom import converters

register_converter(converters.IDConverter, "idencode")

schema_view = get_schema_view(
    openapi.Info(
        title="leadtracker_v1",
        default_version="v1",
        description="APIs availabe for leadtracker_v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("djadmin/", admin.site.urls),
    path("__debug__/", include(debug_toolbar.urls)),
    # Apps
    url("v1/accounts/", include("v1.accounts.urls")),
    url("v1/communications/", include("v1.communications.urls")),
    url("v1/leadtracker/", include("v1.leadtracker.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(
            r"^doc/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    ]
