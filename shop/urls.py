from django.urls import path
from .apps import APP_NAME
app_name=APP_NAME
from . import views
urlpatterns = [
    path('',views.BasicViews().home,name='home')
]
