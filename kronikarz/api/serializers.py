from rest_framework import serializers
from .models import (
    Event,
    FamilyTree,
    Mariage,
    Media,
    Person,
)

from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_serializer_method

User = get_user_model()


class BasicFamilyTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyTree
        fields = [
            'id',
            'name',
            'description',
        ]


class MariageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mariage
        fields = [
            'id',
            'person_1',
            'person_2',
            'mariage_date',
            'divorce_date'
        ]

    def to_internal_value(self, data):
        if(data['mariage_date'] == ''):
            data['mariage_date'] = None
        if(data['divorce_date'] == ''):
            data['divorce_date'] = None
        return super().to_internal_value(data)


class BasicPersonSerializer(serializers.ModelSerializer):
    mariages = MariageSerializer(many=True)
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = [
            'id',
            'name',
            'surname',
            'x',
            'y',
            'sex',
            'mariages',
            'profile_pic'
        ]

    @swagger_serializer_method(serializers.ImageField)
    def get_profile_pic(self, obj):
        media = Media.objects.filter(
            person__pk=obj.pk, is_profile_pic=True).first()
        if media is not None:
            file_url = self.context['request'].build_absolute_uri(
                media.file.url)
            return file_url
        else:
            return ''


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'person',
            'title',
            'description',
            'date',
            'icon'
        ]

    def to_internal_value(self, data):
        if(data['date'] == ''):
            data['date'] = None
        return super().to_internal_value(data)


class FamilyTreeSerializer(serializers.ModelSerializer):
    persons = BasicPersonSerializer(many=True)

    class Meta:
        model = FamilyTree
        fields = [
            'id',
            'name',
            'description',
            'persons',
        ]


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            'id',
            'person',
            'name',
            'file',
            'is_profile_pic'
        ]


class PersonSerializer(serializers.ModelSerializer):
    medias = MediaSerializer(many=True, read_only=True)
    events = EventSerializer(many=True, read_only=True)
    mariages = MariageSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = [
            'id',
            'family_tree',
            'father',
            'mother',
            'name',
            'surname',
            'x',
            'y',
            'birth_date',
            'nationality',
            'sex',
            'birth_place',
            'death_date',
            'death_cause',
            'medias',
            'events',
            'mariages'
        ]

    def to_internal_value(self, data):
        if(data['birth_date'] == ''):
            data['birth_date'] = None
        if(data['death_date'] == ''):
            data['death_date'] = None
        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

        return user
