from adminplus.sites import AdminSitePlus
from django.conf.urls import url, include
from django.contrib import admin

from . import views

app_name = 'arbuz_core'

urlpatterns = [
    url(r'^buildings/', views.BuildingListView.as_view()),
    url(r'^dump/', views.dump),
    url(r'^$', views.index_view),
]
