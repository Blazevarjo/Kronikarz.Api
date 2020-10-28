from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import (
    Event,
    FamilyTree,
    Mariage,
    Media,
    Person,
    User
)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

admin.site.register((Event, FamilyTree, Mariage, Media, Person))
