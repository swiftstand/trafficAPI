from django.urls import path,include
from Traffic.api import views as traffic_api_views
app_name = 'traffic'

urlpatterns = [
    path('updates/<str:localty>', traffic_api_views.getupdates, name="updates"),
    path('updates/create/', traffic_api_views.createupdate, name="create"),
]