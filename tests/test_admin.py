from django.test import TestCase
from django_admin_groups.admin import CustomAdminSite

class CustomAdminSiteTest(TestCase):
    def test_admin_site_creation(self):
        admin_site = CustomAdminSite()
        self.assertIsNotNone(admin_site)
