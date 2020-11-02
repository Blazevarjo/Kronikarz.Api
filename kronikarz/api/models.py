from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from django.db import models


class Event(models.Model):
    class Icons(models.TextChoices):
        OTHER = 'OTHER', _("Other")
        # Develop more icons

    person = models.ForeignKey('api.Person', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000, null=True)
    date = models.DateField(null=True)
    icon = models.CharField(
        max_length=20, choices=Icons.choices, default=Icons.OTHER)


class FamilyTree(models.Model):
    user = models.ForeignKey('api.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=10000, null=True)


class Mariage(models.Model):
    person_1 = models.ForeignKey(
        'api.Person', related_name='person_1', on_delete=models.CASCADE)
    person_2 = models.ForeignKey(
        'api.Person', related_name='person_2', on_delete=models.CASCADE)
    mariage_date = models.DateField(null=True)
    divorce_date = models.DateField(null=True)


def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/filename'


class Media(models.Model):
    person = models.ForeignKey('api.Person', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to=user_directory_path)


class Person(models.Model):
    class Sex(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    family_tree = models.ForeignKey('api.FamilyTree', on_delete=models.CASCADE)
    father = models.ForeignKey(
        'api.Person',  null=True, on_delete=models.SET_NULL, related_name='person_father')
    mother = models.ForeignKey(
        'api.Person', null=True, on_delete=models.SET_NULL, related_name='person_mother')
    name = models.CharField(max_length=50, null=True)
    surname = models.CharField(max_length=50, null=True)
    birth_date = models.DateField(null=True)
    # think about enum or another class, django-countries?
    nationality = models.CharField(max_length=100, null=True)
    sex = models.CharField(max_length=6, choices=Sex.choices, null=True)
    birth_place = models.CharField(max_length=150, null=True)
    death_date = models.DateField(null=True)
    death_cause = models.CharField(max_length=200, null=True)


class User(AbstractUser):
    pass
