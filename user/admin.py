from django.contrib import admin
from django.contrib.auth.models import Group
from modeltranslation.admin import TranslationAdmin

from .models import User, VerifyEmail, CardData
from django.contrib.sites.models import Site


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone', 'money', 'user_type')
    readonly_fields = ('money', 'rating',)


class VerifEmailAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code')


class CardAdmin(admin.ModelAdmin):
    list_display = ('card', 'account')


admin.site.register(User, UserAdmin)
admin.site.register(VerifyEmail, VerifEmailAdmin)
admin.site.register(CardData, CardAdmin)
admin.site.unregister(Site)
admin.site.unregister(Group)