from django.views.decorators import csrf
from django.utils.decorators import method_decorator
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import (
    status,
    views,
    viewsets,
)

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
    PersonSerializer, UserSerializer,
)

from .permissions import (
    IsEventOwner,
    IsFamilyTreeOwner,
    IsMariageOwner, IsMediaOwner,
    IsPersonOwner
)

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login
)
User = get_user_model()


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
        if self.action in ['list', 'create']:
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


# Register and login

@method_decorator(csrf.csrf_protect, name='dispatch')
class LoginView(views.APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']

        if username is None or password is None:
            raise ValidationError("Please enter both username and password")

        user = authenticate(username=username, password=password)

        print('authenticate: ' + str(user))

        if user is not None:
            login(request, user)
            return Response(
                {'detail': 'Success'},
                status=status.HTTP_200_OK)
        else:
            raise ValidationError('Invalid credentials')


@method_decorator(csrf.requires_csrf_token, name='dispatch')
class RegisterView(views.APIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            login(request, user)
            return Response(
                {'detail': f'Successfully registeres new user: {user.username}'},
                status=status.HTTP_201_CREATED)


# Generate CSRF TOKEN


@method_decorator(csrf.ensure_csrf_cookie, name='dispatch')
class CSRFTokenView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return Response({'detail': 'Success, SCRF cookie set'},
                        status=status.HTTP_200_OK)
