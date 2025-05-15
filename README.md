# Django Admin Groups

*Combine models from different apps under a single label in the admin panel.*


## Installation
- Install the package using pip:

    ```bash
    pip install django-admin-groups
    ```


- Add `django_admin_groups` to your `INSTALLED_APPS`:

    you should add it before the "django.contrib.admin"
    ```python
    INSTALLED_APPS = [
        ...
        "django_admin_groups",
        "django.contrib.admin"
    ]
    ```

## Usage

- Define your custom groups in the `settings.py` file using the `ADMIN_GROUPS` setting.

    Each group includes:

    - **`group_name`:** The name displayed in the admin panel.
    - **`models`:** A list of model paths in the format `app_label.ModelName`.

    Example:
    ```python
    ADMIN_GROUPS = [
        {
            "group_name": "group_1",
            "models": [
                "app_1.model1",
                "app_2.model2",
            ],
        },
        {
            "group_name": "group_2",
            "models": [
                "app_1.model3",
                "app_2.model4",
            ],
        },
    ]
    ```


- add the "admin-groups_context" to the templates context_processors

    ```python
    TEMPLATES = [
        {
            ...
            "OPTIONS": {
                "context_processors": [
                    ...
                    "django_admin_groups.context_processors.admin_groups_context",
                ],
            },
        },
    ]

    ```


- Use the custom admin site provided by the package in your `admin.py`:
    ```python
    from django_admin_groups.admin import CustomAdminSite
    from app_1.models import model_1, model_2
    from app_2.models import model_3, model_4


    custom_admin_site = CustomAdminSite()
    custom_admin_site.register(model_1)
    custom_admin_site.register(model_2)
    custom_admin_site.register(model_3)
    custom_admin_site.register(model_4)
    ```

- Route your admin URLs to use the custom admin site in `urls.py`:
    ```python
    from django.urls import path from django_admin_groups.admin import custom_admin_site


    urlpatterns = [
        re_path( # urls for the custom app_index pages 
            r"^admin/(?P<group_name>[\w-]+)/$",
            custom_admin_site.group_index,
            name="admin_group_index"
        ),
        path("admin/", custom_admin_site.urls),  
    ]
    ```

## How It Works
This package overrides Django’s get_app_list and _build_app_dict to use your ADMIN_GROUPS instead of the default app-based layout.

- Group names appear exactly in the order you define them.

- Models within groups also respect your defined order.

- Breadcrumbs and section labels reflect group names instead of app labels.

If you override any of the default Django admin templates (like change_list.html, change_form.html, etc.), and you want the custom breadcrumbs to work correctly inside your templates, simply include the shared breadcrumb partial:

```django
{% include "django_admin_groups/breadcrumbs.html" with action="Edit" %}

```

action is optional and can be "Edit", "Add" — or left blank.


---

## License

This project is licensed under the **MIT License**. See the LICENSE file for details.

---

## Contribution

We welcome contributions!
If you have ideas, suggestions, or bug reports, please open an issue or submit a pull request.

### Steps to Contribute:

1. Fork the repository.
2. Clone your forked repository.
3. Create a feature branch.
4. Make your changes and add tests (if necessary).
5. Submit a pull request.

[GitHub repository](https://github.com/OmarSwailam/django-admin-groups).
[PyPi](https://pypi.org/project/django-admin-groups/).
---

Author: Omar Swailam