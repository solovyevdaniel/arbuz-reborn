"""arbuz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from adminplus.sites import AdminSitePlus
from django.conf.urls import url, include
from django.contrib import admin

from arbuz_core import views

admin.site = AdminSitePlus()
admin.sites.site = admin.site
admin.autodiscover()

urlpatterns = [
    url(r'^admin/send_letter/', views.send_letter),
    url(r'^admin/parse_data/', views.parse_data),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('arbuz_core.urls')),
]

