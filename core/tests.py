
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

from .models import Item


class LostFoundProjectTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPassword123'
        )

        self.item = Item.objects.create(
            item_type='Lost',
            item_name='Test Mobile',
            category='Electronics',
            description='A test mobile phone',
            location='College Campus',
            date_lost_found=date.today(),
            contact_number='9876543210',
            status='Active',
            reported_by=self.user
        )

    def test_homepage_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_item_list_loads(self):
        response = self.client.get(reverse('item_list'))
        self.assertEqual(response.status_code, 200)

    def test_item_detail_loads(self):
        response = self.client.get(
            reverse('item_detail', args=[self.item.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_report_lost_requires_login(self):
        response = self.client.get(reverse('report_lost'))
        self.assertEqual(response.status_code, 302)

    def test_report_found_requires_login(self):
        response = self.client.get(reverse('report_found'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_open_dashboard(self):
        self.client.login(
            username='testuser',
            password='TestPassword123'
        )

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_item_is_saved(self):
        self.assertEqual(Item.objects.count(), 1)

    def test_item_name_is_correct(self):
        self.assertEqual(self.item.item_name, 'Test Mobile')
