from django.contrib import admin
from .models import User, Cargo

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

admin.site.register(User, UserAdmin)


class CargoAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'description')

admin.site.register(Cargo, CargoAdmin)