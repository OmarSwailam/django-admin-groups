from django.apps import apps
from django.conf import settings
from django.contrib.admin import AdminSite
from django.urls import reverse


class CustomAdminSite(AdminSite):
    def __init__(self, *args, **kwargs):
        self.site_header = getattr(settings, "ADMIN_SITE_HEADER", "Django Admin")
        self.site_title = getattr(settings, "ADMIN_SITE_TITLE", "Django Admin")
        self.index_title = getattr(
            settings, "ADMIN_INDEX_TITLE", "Welcome to Django Admin"
        )
        super().__init__(*args, **kwargs)

    def get_app_list(self, request, *args, **kwargs):
        app_list = []
        admin_reorder_config = getattr(settings, "ADMIN_GROUPS", [])

        grouped_models = {}

        for group_config in admin_reorder_config:
            group_name = group_config.get("group_name")
            models_config = group_config.get("models", [])

            for model_name in models_config:
                app_label, model_name = model_name.split(".")
                model = apps.get_model(app_label, model_name)

                model_admin = self._registry.get(model)
                if model_admin and not model_admin.has_view_permission(request):
                    continue

                if group_name not in grouped_models:
                    grouped_models[group_name] = []

                model_url = reverse(
                    "admin:%s_%s_changelist" % (app_label, model_name.lower())
                )

                grouped_models[group_name].append(
                    {
                        "name": model._meta.verbose_name_plural,
                        "object_name": model.__name__,
                        "admin_url": model_url,
                    }
                )

        for group_name, models in grouped_models.items():
            app_list.append(
                {"app_label": group_name, "name": group_name, "models": models}
            )

        return app_list
