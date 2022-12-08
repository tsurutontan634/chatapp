# Register your models here.
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


from .models import UserManager,CustomUser,Talk

#admin.site.register(UserManager)
admin.site.register(CustomUser)
admin.site.register(Talk)