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
    BasicFamilyTreeSerializer,
    FamilyTreeSerializer,
    MariageSerializer,
    MediaSerializer,
    PersonSerializer,
)

from .permissions import (
    IsOwner
)


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        current_user = self.request.user
        return Event.objects.filter(person__family_tree__user=current_user)


class FamilyTreeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]

    def get_queryset(self):
        current_user = self.request.user
        return FamilyTree.objects.filter(user=current_user)

    def get_serializer_class(self):
        if self.action == 'list':
            return BasicFamilyTreeSerializer
        else:
            return FamilyTreeSerializer


class MariageViewSet(viewsets.ModelViewSet):
    queryset = Mariage.objects.all()
    serializer_class = MariageSerializer

    def get_queryset(self):
        current_user = self.request.user
        return Mariage.objects.filter(person_1__family_tree__user=current_user)


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def get_queryset(self):
        current_user = self.request.user
        return Media.objects.filter(person__family_tree__user=current_user)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get_queryset(self):
        current_user = self.request.user
        return Person.objects.filter(family_tree__user=current_user)
