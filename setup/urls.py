from django.contrib import admin
from django.urls import path
from biotech.views import telainicial


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", telainicial, name="telainicial"),
]
