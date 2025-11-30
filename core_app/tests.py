from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Attendance
from io import BytesIO

class BasicFlowTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_register_and_attendance_endpoints(self):
        # create a small fake image bytes (not a valid jpeg but sufficient for upload handling)
        fake_image = BytesIO(b'\x00\x01\x02\x03')
        fake_image.name = 'capture.jpg'

        # register
        resp = self.client.post(reverse('register_submit'), {
            'userid': 'u1',
            'name': 'Test User'
        }, format='multipart', files={'image': fake_image})
        self.assertIn(resp.status_code, (200, 201))

        # attendance
        fake_image2 = BytesIO(b'\x00\x01\x02\x03')
        fake_image2.name = 'att.jpg'
        resp2 = self.client.post(reverse('attendance_submit'), {
            'userid': 'u1'
        }, format='multipart', files={'image': fake_image2})
        self.assertIn(resp2.status_code, (200, 201))
