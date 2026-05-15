from django.apps import AppConfig


class PlacesConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'

    name = 'apps.places'

    def ready(self):
        from smart_tourism.compat import patch_django_template_context_copy

        patch_django_template_context_copy()
