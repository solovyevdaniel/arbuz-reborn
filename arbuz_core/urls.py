from adminplus.sites import AdminSitePlus
from django.conf.urls import url, include
from django.contrib import admin

from arbuz_core import views
from arbuz_core.views import BuildingListView

app_name = 'arbuz_core'

urlpatterns = [
    url(r'^all/', BuildingListView.as_view()),
    url(r'^crimes_grid/$', views.get_crimes_grid),
]
