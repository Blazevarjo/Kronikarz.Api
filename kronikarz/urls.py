"""kronikarz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.urls.conf import re_path
from rest_framework import (
    routers,
    permissions
)

from .api.views import (
    CSRFTokenView,
    EventViewSet,
    FamilyTreeViewSet,
    LoginView,
    LogoutView,
    MariageViewSet,
    MediaViewSet,
    PersonViewSet,
    RegisterView
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Kronikarz API",
        default_version='v1',
        contact=openapi.Contact(url="https://github.com/KronikarzIO"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


router = routers.DefaultRouter()

router.register(r'events', EventViewSet, 'event')
router.register(r'family-trees', FamilyTreeViewSet, 'familytree')
router.register(r'mariages', MariageViewSet, 'mariage')
router.register(r'medias', MediaViewSet, 'media')
router.register(r'persons', PersonViewSet, 'person')


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'auth/register/', RegisterView.as_view()),
    path(r'auth/login/', LoginView.as_view()),
    path(r'auth/logout/', LogoutView.as_view()),

    path(r'auth/csrf-cookie/', CSRFTokenView.as_view()),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', schema_view.with_ui('swagger',
                                          cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc',
                                        cache_timeout=0), name='schema-redoc'),
]

urlpatterns += router.urls
