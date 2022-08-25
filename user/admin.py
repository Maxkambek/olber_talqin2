from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import User, Cargo, VerifyEmail, Work


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'money', 'car_type')
    readonly_fields = ('rating',)
    list_editable = ('car_type',)


class CargoAdmin(TranslationAdmin):
    list_display = ('title', 'price', 'status', 'cargo_type', 'description', 'distance')
    readonly_fields = ('from_address', 'to_address', 'distance', 'doer')


class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'description', 'image')


class VerifEmailAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code')


admin.site.register(User, UserAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(VerifyEmail, VerifEmailAdmin)