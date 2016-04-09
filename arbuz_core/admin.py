from django.contrib import admin
from arbuz_core.models import Building, Crimes

# class BuildingAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Building, BuildingAdmin)

admin.site.register(Building)
admin.site.register(Crimes)
