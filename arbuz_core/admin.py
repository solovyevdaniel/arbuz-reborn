from django.contrib import admin

from arbuz_core import views
from arbuz_core.models import Building, Crimes, AdminUser

# class BuildingAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Building, BuildingAdmin)

admin.site.register(Building)
admin.site.register(Crimes)
admin.site.register(AdminUser)

admin.site.register_view('send_letter', 'Send letter', view=views.get_send_letter_form)
admin.site.register_view('parse_data', 'Parse data from .xls', view=views.get_parse_data_form)
