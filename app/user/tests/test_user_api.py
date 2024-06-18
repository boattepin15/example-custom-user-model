from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status




#กำนหด Url สมัครสมาชิก user/create
CREATE_USER_URL = reverse('user:create')
#กำหนด url สร้าง token user/token
TOKEN_USER = reverse('user:token')



class PublicUserApiTests(TestCase):
    """ สร้าง Test API ของ User แบบ Public"""

    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_success(self):
        """ทดสอบ API สมัคร สมาชิก"""
        payload = {
            "email":'email@test.com',
            'username':'username',
            'password':'password1234'
        }
        #ทดสอบ request ไปยัง API method post -> /api/user/create 
        res = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(username=payload['username'])
        #ทดสอบว่าสมัครสมาชิกใหม่ได้
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        #ทดสอบว่าการเข้ารหัสถูกต้อง
        self.assertTrue(user.check_password(payload['password']))
        #ทดสอบว่าจะไม่มีการส่ง password กลับมาผ่าน respone
        self.assertNotIn('password', res.data)
    
    def test_user_with_email_exists_error(self):
        """ทดสอบ ขั้นตอนสมัคร เช็คว่ามีผู้ใช้งานที่เราสมัครไปแล้ว"""
        payload = {
            "email":'email@test.com',
            'username':'username',
            'password':'password1234'
        }
        get_user_model().objects.create_user(
            email=payload['email'],
            username=payload['username'],
            password=payload['password']
        )
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_shrot_error(self):
        """ทดสอบว่า password มีความยาวน้อยกว่ากำหนดหรือไม่"""
        payload = {
            "email":'email@test.com',
            'username':'username',
            'password':'pass'
        }
        res = self.client.post(CREATE_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_create_token_for_user(self):
        """ ทดสอบสร้าง token สำหรับ valid credentials """
        user_details = {
            "email": 'test@gmail.com',
            "username": 'Test Name',
            "password": 'test-user-password12345'
        }
        user = get_user_model().objects.create_user(
            email=user_details['email'],
            username=user_details['username'],
            password=user_details['password']
            
        )
        payload = {
            'username': user_details['username'],
            'password': user_details['password']
        }
        res = self.client.post(TOKEN_USER, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)