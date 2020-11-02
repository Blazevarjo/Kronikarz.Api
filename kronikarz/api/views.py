from rest_framework import viewsets

from .models import (
    Event,
    FamilyTree,
    Mariage,
    Media,
    Person,
)
from .serializers import (
    EventSerializer,
    FamilyTreeSerializer,
    MariageSerializer,
    MediaSerializer,
    PersonSerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class FamilyTreeViewSet(viewsets.ModelViewSet):
    queryset = FamilyTree.objects.all()
    serializer_class = FamilyTreeSerializer


class MariageViewSet(viewsets.ModelViewSet):
    queryset = Mariage.objects.all()
    serializer_class = MariageSerializer


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
