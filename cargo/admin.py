from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from cargo.models import Cargo


class CargoAdmin(TranslationAdmin):
    list_display = ('title', 'price', 'status', 'cargo_type', 'description', 'distance')
    readonly_fields = ('from_address', 'to_address', 'distance', 'doer')

admin.site.register(Cargo, CargoAdmin)
