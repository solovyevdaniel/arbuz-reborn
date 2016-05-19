from django.conf.urls import url, include
from arbuz_core.views import BuildingListView

app_name = 'arbuz_core'

urlpatterns = [
    url(r'^all/', BuildingListView.as_view()),
]
