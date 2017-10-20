# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from LunchCloud.models import FoodType, InvitationCode, Profile, LunchEvents


class FoodTypeAdmin(admin.ModelAdmin):
    pass


class InvitationCodeAdmin(admin.ModelAdmin):
    pass


class LunchEventsAdmin(admin.ModelAdmin):
    pass


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(LunchEvents, LunchEventsAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(FoodType, FoodTypeAdmin)
admin.site.register(InvitationCode, InvitationCodeAdmin)
