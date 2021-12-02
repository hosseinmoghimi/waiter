from authentication.apps import APP_NAME
from django.apps import AppConfig

APP_NAME='core'
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
