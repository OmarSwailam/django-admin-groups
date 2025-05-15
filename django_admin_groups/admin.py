from django.apps import apps
from django.conf import settings
from django.contrib.admin import AdminSite
from django.urls import reverse, NoReverseMatch
from django.template.response import TemplateResponse
from django.utils.text import capfirst
from django.utils.text import slugify


class CustomAdminSite(AdminSite):
    def __init__(self, *args, **kwargs):
        self.site_header = getattr(settings, "ADMIN_SITE_HEADER", "Django Admin")
        self.site_title = getattr(settings, "ADMIN_SITE_TITLE", "Django Admin")
        self.index_title = getattr(
            settings, "ADMIN_INDEX_TITLE", "Welcome to Django Admin"
        )
        super().__init__(*args, **kwargs)

    def group_index(self, request, group_name):
        app_list = self.get_app_list(request, group_name=group_name)

        context = dict(self.each_context(request))
        context.update({
            "title": group_name,
            "app_label": group_name,
            "app_list": app_list,
        })

        return TemplateResponse(request, "admin/app_index.html", context)
    
    def each_context(self, request):
        context = super().each_context(request)

        try:
            resolver_match = request.resolver_match
            url_name = resolver_match.url_name
            parts = url_name.split("_")[:-1]
            app_label = "_".join(parts[:-1])
            model_name = parts[-1]
            context["model_key"] = f"{app_label}.{model_name}".lower()
            context["resolved_model_label"] = app_label
            context["resolved_model_name"] = model_name
        except Exception:
            pass
        
        return context

    def _build_app_list(self, request, label=None, group_name=None):
        app_list = []

        admin_groups = getattr(settings, "ADMIN_GROUPS", [])

        for group in admin_groups:
            full_group_name = group["group_name"]
            group_slug = slugify(full_group_name)

            if group_name and slugify(group_name) != group_slug:
                continue

            model_keys = group["models"]
            model_list = []

            for model_path in model_keys:
                app_label, model_name = model_path.split(".")
                model = apps.get_model(app_label, model_name.lower())

                if model not in self._registry:
                    continue

                model_admin = self._registry[model]

                if not model_admin.has_module_permission(request):
                    continue

                perms = model_admin.get_model_perms(request)
                if not any(perms.values()):
                    continue

                info = (app_label, model._meta.model_name)
                model_dict = {
                    "model": model,
                    "name": capfirst(model._meta.verbose_name_plural),
                    "object_name": model._meta.object_name,
                    "perms": perms,
                    "admin_url": None,
                    "add_url": None,
                }

                if perms.get("change") or perms.get("view"):
                    model_dict["view_only"] = not perms.get("change")
                    try:
                        model_dict["admin_url"] = reverse(
                            f"admin:{app_label}_{model._meta.model_name}_changelist",
                            current_app=self.name,
                        )
                    except NoReverseMatch:
                        pass

                if perms.get("add"):
                    try:
                        model_dict["add_url"] = reverse(
                            f"admin:{app_label}_{model._meta.model_name}_add",
                            current_app=self.name,
                        )
                    except NoReverseMatch:
                        pass

                model_list.append(model_dict)

            if model_list:
                app_list.append({  
                    "name": full_group_name,
                    "app_label": full_group_name,
                    "app_url": reverse("admin_group_index", args=[group_slug]),
                    "has_module_perms": True,
                    "models": model_list,
                })

        return app_list

    def get_app_list(self, request, app_label=None, *args, **kwargs):
        group_name = kwargs.get("group_name")
        return self._build_app_list(request, label=app_label, group_name=group_name)