from django.conf.urls import url, include
from . import views

app_name = 'arbuz_core'

urlpatterns = [
    url(r'^all-crimes/', views.BuildingListView.as_view()),
    url(r'^dump/', views.dump),
]
