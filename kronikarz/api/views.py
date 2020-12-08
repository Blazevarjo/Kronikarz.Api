from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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
    IsEventOwner,
    IsFamilyTreeOwner,
    IsMariageOwner, IsMediaOwner,
    IsPersonOwner
)


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsEventOwner]

    def get_queryset(self):
        current_user = self.request.user
        return Event.objects.filter(person__family_tree__user=current_user)


class FamilyTreeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsFamilyTreeOwner]

    def get_queryset(self):
        current_user = self.request.user
        return FamilyTree.objects.filter(user=current_user)

    def get_serializer_class(self):
        if self.action == 'list':
            return BasicFamilyTreeSerializer
        else:
            return FamilyTreeSerializer


class MariageViewSet(viewsets.ModelViewSet):
    serializer_class = MariageSerializer
    permission_classes = [IsAuthenticated, IsMariageOwner]

    def get_queryset(self):
        current_user = self.request.user
        return Mariage.objects.filter(person_1__family_tree__user=current_user)


class MediaViewSet(viewsets.ModelViewSet):
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated, IsMediaOwner]

    def get_queryset(self):
        current_user = self.request.user
        return Media.objects.filter(person__family_tree__user=current_user)


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated, IsPersonOwner]

    def get_queryset(self):
        current_user = self.request.user
        return Person.objects.filter(family_tree__user=current_user)
