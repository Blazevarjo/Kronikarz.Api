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
from rest_framework import routers

from .api.views import (
    CSRFTokenView,
    EventViewSet,
    FamilyTreeViewSet,
    LoginView,
    MariageViewSet,
    MediaViewSet,
    PersonViewSet,
    RegisterView
)


router = routers.DefaultRouter()

router.register(r'events', EventViewSet, 'event')
router.register(r'family-trees', FamilyTreeViewSet, 'familytree')
router.register(r'mariages', MariageViewSet, 'mariage')
router.register(r'medias', MediaViewSet, 'media')
router.register(r'persons', PersonViewSet, 'person')


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'register/', RegisterView.as_view()),
    path(r'login/', LoginView.as_view()),
    path(r'csrf-cookie/', CSRFTokenView.as_view())
]

urlpatterns += router.urls
