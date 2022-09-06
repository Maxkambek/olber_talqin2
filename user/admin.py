from django.contrib import admin
from django.contrib.auth.models import Group
from modeltranslation.admin import TranslationAdmin

from .models import User, Cargo, VerifyEmail, Work, CardData
from django.contrib.sites.models import Site


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone', 'money', 'user_type')
    readonly_fields = ('money', 'rating',)


class CargoAdmin(TranslationAdmin):
    list_display = ('title', 'price', 'status', 'cargo_type', 'description', 'distance')
    readonly_fields = ('from_address', 'to_address', 'distance', 'doer')


class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'description', 'image')


class VerifEmailAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code')


class CardAdmin(admin.ModelAdmin):
    list_display = ('card', 'account')


admin.site.register(User, UserAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(VerifyEmail, VerifEmailAdmin)
admin.site.register(CardData, CardAdmin)
admin.site.unregister(Site)
admin.site.unregister(Group)