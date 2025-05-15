from django.conf import settings

def admin_groups_context(request):
    return {
        "admin_groups": getattr(settings, "ADMIN_GROUPS", [])
    }