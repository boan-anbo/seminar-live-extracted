# Create your tests here.
import json

from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory


class UserProfileTests(APITestCase):
    def test_get_profile(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('userprofile-list')
        print(url)

        factory = APIRequestFactory()
        # user = User.objects.get(username='bo')

        request = factory.get(url)
        # force_authenticate(request, user=user)


        # data = {
        #     'title': 'test webinar',
        #     'summary': 'webinar summary',
        #     'startDateTime': timezone.now(),
        # }
        # response = self.client.post(url, data, format='json')
        response = self.client.get(url, format='json')

        # print(response)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(response.data, data)


        # response = self.client.get(url)
        jsonResponse = json.loads(response.content)
        print(jsonResponse)
        # self.assertIsNotNone(len(jsonResponse['results']) == 2)