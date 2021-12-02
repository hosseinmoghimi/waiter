from .apps import APP_NAME
from . import views,apis
from django.urls import path

app_name=APP_NAME
urlpatterns = [
    path("",views.BasicViews().home,name="home"),
    path("search/",views.BasicViews().home,name="search"),
    path("parameters/<app_name>/",views.BasicViews().parameters,name="parameters"),
    path("profile_customization/",views.BasicViews().home,name="profile_customization"),
    path("change_parameters/<app_name>/",views.BasicViews().home,name="change_parameters"),
    path("notifications/",views.BasicViews().home,name="notifications"),
]
