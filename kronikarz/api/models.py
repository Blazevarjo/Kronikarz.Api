from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from django.db import models


class Event(models.Model):
    class Icons(models.TextChoices):
        PRIZE = 'PRIZE', _("Prize")
        SCIENCE = 'SCIENCE', _("Science")
        OTHER = 'OTHER', _("Other")

    person = models.ForeignKey(
        'api.Person', related_name='events', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000, blank=True)
    date = models.DateField(blank=True, null=True)
    icon = models.CharField(
        max_length=20, choices=Icons.choices, default=Icons.OTHER)


class FamilyTree(models.Model):
    user = models.ForeignKey('api.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=10000, blank=True)


class Mariage(models.Model):
    person_1 = models.ForeignKey(
        'api.Person', related_name='mariages', on_delete=models.CASCADE)
    person_2 = models.ForeignKey(
        'api.Person', related_name='person_2', on_delete=models.CASCADE)
    mariage_date = models.DateField(blank=True, null=True)
    divorce_date = models.DateField(blank=True, null=True)


def user_directory_path(instance, filename):
    return f'user_{instance.person.family_tree.user.id}/{filename}'


class Media(models.Model):
    person = models.ForeignKey(
        'api.Person', related_name='medias', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to=user_directory_path)
    is_profile_pic = models.BooleanField(default=False)


class Person(models.Model):
    class Sex(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    family_tree = models.ForeignKey(
        'api.FamilyTree', related_name='persons', on_delete=models.CASCADE)
    father = models.ForeignKey(
        'api.Person', blank=True, null=True, on_delete=models.SET_NULL, related_name='person_father')
    mother = models.ForeignKey(
        'api.Person', blank=True, null=True, on_delete=models.SET_NULL, related_name='person_mother')
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    x = models.FloatField()
    y = models.FloatField()
    birth_date = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True)
    sex = models.CharField(max_length=6, choices=Sex.choices, blank=True)
    birth_place = models.CharField(max_length=150, blank=True)
    death_date = models.DateField(blank=True, null=True)
    death_cause = models.CharField(max_length=200, blank=True)


class User(AbstractUser):
    pass
