"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

swagger_info = openapi.Info(
    title="Snippets API",
    default_version="v1",
    description="""EduClass project.""",
    terms_of_service="https://www.google.com/policies/terms/",
    license=openapi.License(name="Private")
)

schema_view = get_schema_view(
    info=swagger_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('organizations/', include('apps.organizations.urls')),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path(r'redoc-old/', schema_view.with_ui('redoc-old', cache_timeout=0), name='schema-redoc-old'),

    re_path(r'cached/swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=None), name='cschema-json'),
    path(r'cached/swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='cschema-swagger-ui'),
    path(r'cached/redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='cschema-redoc'),

    path("admin/", admin.site.urls),

]
