from rest_framework.test import APITestCase
from django.urls import reverse
# from faker import Faker

from authentication.models import User


class TestSetUp(APITestCase):

    def setUp(self):

        self.register_url = reverse('register')
        self.login_url = reverse('login')

        self.password_reset_request_url = reverse('request-reset-email')
        self.password_reset_complete_url = reverse('password-reset-complete')

        # self.fake = Faker()

        # self.user_data = {
        #     'email': self.fake.email(),
        #     'username': self.fake.email().split('@')[0],
        #     'password': self.fake.email(),
        # }

        self.user_reset_data = {
            'password': 'powerfrontend',
            'token': '1123eeddfrryhfjudoks-029976ydbbsjsnj',
            'uidb64': 'MTA',
        }


    # def test_user_cannot_register_with_no_data(self):
    #     res = self.client.post(self.register_url)
    #     self.assertEqual(res.status_code, 400)

    # def test_user_can_register_correctly(self):
    #     res = self.client.post(
    #         self.register_url, self.user_data, format="json")
    #     self.assertEqual(res.data['email'], self.user_data['email'])
    #     self.assertEqual(res.data['username'], self.user_data['username'])
    #     self.assertEqual(res.status_code, 201)

    # def test_user_cannot_login_with_unverified_email(self):
    #     self.client.post(
    #         self.register_url, self.user_data, format="json")
    #     res = self.client.post(self.login_url, self.user_data, format="json")
    #     self.assertEqual(res.status_code, 401)

    # def test_user_can_login_after_verification(self):
    #     response = self.client.post(
    #         self.register_url, self.user_data, format="json")
    #     email = response.data['email']
    #     user = User.objects.get(email=email)
    #     user.is_verified = True
    #     user.save()
    #     res = self.client.post(self.login_url, self.user_data, format="json")
    #     self.assertEqual(res.status_code, 200)
########################################################################


    def test_user_must_be_authenthicated_to_reset(self):
        res = self.client.post(
            self.password_reset_complete_url, self.user_reset_data, format="json")
        self.assertEqual(res.status_code, 405)

    def test_user_cannot_reset_with_wrong_data(self):
        res = self.client.post(self.password_reset_complete_url,
                self.user_reset_data,format="json")
        self.assertNotEqual(res.status_code, 200)

    def test_user_reset_not_a_redirection(self):
        res = self.client.post(self.password_reset_complete_url,
        self.user_reset_data,format="json")
        self.assertNotEqual(res.status_code, 200)

    def test_user_reset_not_a_page_not_found(self):
        res = self.client.post(self.password_reset_complete_url,
        self.user_reset_data,format="json")
        self.assertNotEqual(res.status_code, 404)

    def test_user_reset_endpoint_valid(self):
        res = self.client.post(self.password_reset_complete_url,
        self.user_reset_data,format="json")
        self.assertNotEqual(res.status_code, 500)

    
    
        
   
       


    

   





