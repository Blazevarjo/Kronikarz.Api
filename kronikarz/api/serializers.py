from rest_framework import serializers
from .models import (
    Event,
    FamilyTree,
    Mariage,
    Media,
    Person,
)


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
    class Meta:
        model = FamilyTree
        fields = [
            'url',
            'name',
            'description'
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
            'death_cause'
        ]
