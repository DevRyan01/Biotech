from django.contrib import admin
from django.urls import path
from biotech.views import analises, dashboard_list


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", analises, name="analises"),
    path("dashboard/", dashboard_list, name="dashboard"),
]
