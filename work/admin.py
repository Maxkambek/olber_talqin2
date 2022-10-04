from django.contrib import admin

from work.models import Work


class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'description', 'image')


admin.site.register(Work, WorkAdmin)
