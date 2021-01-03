from rest_framework import serializers
from .models import (
    Event,
    FamilyTree,
    Mariage,
    Media,
    Person,
)

from django.contrib.auth import get_user_model

User = get_user_model()


class BasicFamilyTreeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FamilyTree
        fields = [
            'url',
            'name',
            'description',
        ]


class MariageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mariage
        fields = [
            'url',
            'person_1',
            'person_2',
            'mariage_date',
            'divorce_date'
        ]


class BasicPersonSerializer(serializers.HyperlinkedModelSerializer):
    mariages = MariageSerializer(many=True)

    class Meta:
        model = Person
        fields = [
            'url',
            'name',
            'surname',
            'sex',
            'mariages'
        ]


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = [
            'url',
            'person',
            'title',
            'description',
            'date',
            'icon'
        ]


class FamilyTreeSerializer(serializers.HyperlinkedModelSerializer):
    persons = BasicPersonSerializer(many=True)

    class Meta:
        model = FamilyTree
        fields = [
            'url',
            'name',
            'description',
            'persons',
        ]


class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = [
            'url',
            'person',
            'name',
            'file'
        ]


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    medias = MediaSerializer(many=True)
    events = EventSerializer(many=True)
    mariages = MariageSerializer(many=True)

    class Meta:
        model = Person
        fields = [
            'url',
            'family_tree',
            'father',
            'mother',
            'name',
            'surname',
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

    def create(self, validated_data):
        medias_data = validated_data.pop('medias')
        events_data = validated_data.pop('events')
        person = Person.objects.create(**validated_data)
        for media_data in medias_data:
            Media.objects.create(person=person, **media_data)
        for event_data in events_data:
            Event.objects.create(person=person, **event_data)
        return person


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
