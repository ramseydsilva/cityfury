from django.contrib import admin
from cityfury.models import *


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'publish',)

class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'publish', 'city',)

class PostAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "address", "views", "dislikes_count", "flags_count", "created_date")

    def address(self, instance):
        address = ""
        if instance.location_string:
            address += instance.location_string + ", "
        if instance.area:
            address += instance.area.name + ", "
        if instance.city:
            address += instance.city.name + ", "

        return address[:-2]

    def dislikes_count(self, instance):
        return instance.dislikes.count()

    def flags_count(self, instance):
        return instance.flags.count()

class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "website", "phone", "post", "added_by")

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(City, CityAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Country)
admin.site.register(PostFlag)
admin.site.register(Contact, ContactAdmin)
