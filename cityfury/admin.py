from django.contrib import admin
from cityfury.models import *


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'publish',)

class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'publish', 'city',)

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(City, CityAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Country)
admin.site.register(PostFlag)
