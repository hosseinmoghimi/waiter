from .apps import APP_NAME
from django.urls import path
from .views import HelpView
app_name=APP_NAME
urlpatterns = [
    path('',HelpView().index,name="home"),
    path('<app_name>/',HelpView().app,name="app"),
    path('<app_name>/<template>/',HelpView().help,name="help"),
]

