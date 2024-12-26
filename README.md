# Django Admin Groups

*Combine models from different apps under a single label in the admin panel.*


## Installation
- Install the package using pip:

    ```bash
    pip install django-admin-groups
    ```


- Add `django_admin_groups` to your `INSTALLED_APPS`:

    ```python
    INSTALLED_APPS = [
        ...
        "django_admin_groups",
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
        path("admin/", custom_admin_site.urls),  # Use the custom admin site
    ]
    ```

## How It Works

The package overrides the `get_app_list` method of the Django admin site to dynamically create custom groups based on your `ADMIN_GROUPS` configuration. Models retain their default functionality while appearing organized under user-defined labels.

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
---

Author: Omar Swailam