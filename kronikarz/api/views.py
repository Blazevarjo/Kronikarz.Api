from drf_yasg.utils import (
    swagger_auto_schema,
    swagger_serializer_method
)

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
    login,
    logout
)
User = get_user_model()


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsEventOwner]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Event.objects.none()

        current_user = self.request.user
        return Event.objects.filter(person__family_tree__user=current_user)


@method_decorator(swagger_serializer_method(FamilyTreeSerializer),
                  name='retrieve')
@method_decorator(swagger_serializer_method(BasicFamilyTreeSerializer),
                  name='list')
class FamilyTreeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsFamilyTreeOwner]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return FamilyTree.objects.none()

        current_user = self.request.user
        return FamilyTree.objects.filter(user=current_user)

    def get_serializer_class(self):
        if self.action in ['list', 'create']:
            return BasicFamilyTreeSerializer
        else:
            return FamilyTreeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MariageViewSet(viewsets.ModelViewSet):
    serializer_class = MariageSerializer
    permission_classes = [IsAuthenticated, IsMariageOwner]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Mariage.objects.none()

        current_user = self.request.user
        return Mariage.objects.filter(person_1__family_tree__user=current_user)


class MediaViewSet(viewsets.ModelViewSet):
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated, IsMediaOwner]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Media.objects.none()

        current_user = self.request.user
        return Media.objects.filter(person__family_tree__user=current_user)


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated, IsPersonOwner]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Person.objects.none()

        current_user = self.request.user
        return Person.objects.filter(family_tree__user=current_user)


# Register and login

@method_decorator(csrf.csrf_protect, name='dispatch')
class LoginView(views.APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_description="User log in",
                         responses={200: 'Successfully log in user',
                                    400: 'Something went wrong with log in'},
                         request_body=UserSerializer)
    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']

        if username is None or password is None:
            raise ValidationError("Please enter both username and password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(
                {'detail': 'Success'},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf.requires_csrf_token, name='dispatch')
class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Log out current user",
                         responses={200: 'Successfully log out user'})
    def post(self, request, format=None):
        logout(request)
        return Response({'detail': 'Successfully log out'},
                        status=status.HTTP_200_OK)


@method_decorator(csrf.requires_csrf_token, name='dispatch')
class RegisterView(views.APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_description='Register new User',
                         responses={201: 'Successfully registered user',
                                    400: 'Something went wrong with registration'},
                         request_body=UserSerializer)
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            login(request, user)
            return Response(
                {'username':  user.username,
                 'detail': 'Successfully registered user:'},
                status=status.HTTP_201_CREATED)


class IsAuthenticatedView(views.APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_description='Check if User is logged in',
                         responses={201: r'{"user":  "", "detail": "User is not authenticated:"}',
                                    400: r'{"user":  id,   "detail": "User is authenticated:"}'})
    def get(self, request, format=None):
        user = request.user
        print(user)
        print(user.is_authenticated)
        if user.is_authenticated:
            return Response({'user':  user.id,
                             'detail': 'User is authenticated:'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'user':  '',
                             'detail': 'User is not authenticated:'},
                            status=status.HTTP_401_UNAUTHORIZED)


# Generate CSRF TOKEN


@ method_decorator(csrf.ensure_csrf_cookie, name='dispatch')
class CSRFTokenView(views.APIView):
    permission_classes = [AllowAny]

    @ swagger_auto_schema(operation_description='Endpoint to return CSRF token in cookie')
    def get(self, request, format=None):
        return Response({'detail': 'Success, SCRF cookie set'},
                        status=status.HTTP_200_OK)
