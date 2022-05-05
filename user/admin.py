from django.contrib import admin
from .models import User, Cargo, VerifyEmail

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


class CargoAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'description', 'distance')


class VerifEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'code')


admin.site.register(User, UserAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(VerifyEmail, VerifEmailAdmin)