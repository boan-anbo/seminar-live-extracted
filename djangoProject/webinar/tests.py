# Create your tests here.
# Create a JSON POST request
import json

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase


class WebinarTests(APITestCase):
    def test_get_webinars(self):
        """
        Ensure we can create a new account object.
        """

        url = reverse('webinar-list')
        print(url)
        data = {
            'title': 'test webinar',
            'description': 'webinar summary',
            'startDateTime': timezone.now(),
        }
        response = self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')

        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(response.data, data)


        response = self.client.get(url)
        jsonResponse = json.loads(response.content)
        print(jsonResponse)
        self.assertIsNotNone(len(jsonResponse['results']) == 2)