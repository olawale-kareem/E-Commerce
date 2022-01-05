from .test_setup import TestSetup
from ..models import User


class TestViews(TestSetup):

    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_can_register_with_data(self):
        res = self.client.post(
            self.register_url, self.user_data, format="json")
        self.assertEqual(res.data['email'], self.user_data['email'])
        self.assertEqual(res.data['username'], self.user_data['username'])
        self.assertEqual(res.status_code, 201)

    def cannot_login_with_unverified_data(self):
        self.client.post(
            self.register_url, self.user_data, format="json")
        res = self.client.post(
            self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 401)

    def cannot_login_with_verified_data(self):
        response = self.client.post(
            self.register_url, self.user_data, format="json")
        email = response.data['email']
        user = User.objects.get('email')
        user.save()
        res = self.client.post(
            self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)
