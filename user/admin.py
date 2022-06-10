from django.contrib import admin
from .models import User, Cargo, VerifyEmail, Car


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    readonly_fields = ('rating',)

class CargoAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'cargo_type', 'description', 'distance')
    readonly_fields = ('from_address', 'to_address', 'distance', 'doer')


class VerifEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'code')


class CarAdmin(admin.ModelAdmin):
    list_display = ('user', 'car_type', 'drive_doc', 'tech_inspect')



admin.site.register(User, UserAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(VerifyEmail, VerifEmailAdmin)