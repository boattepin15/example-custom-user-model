from django.test import TestCase
from django.contrib.auth import get_user_model




class Tests_Model(TestCase):
    """ Class สำหรับ TestCase Models"""

    def test_create_user_success(self):
        """ ทดสอบ Model User และทดสอบการสร้าง ผู้ใช้งานหรือฟังก์ชัน create_user"""
        playload = {
            'email':'email@test.com',
            'username':'username',
            'password':'password1234'
        }
        #สร้าง User จาก ฟังก์ชัน get_user_model
        user = get_user_model().objects.create_user(
                email=playload['email'],
                username=playload['username'],
                password=playload['password']
            )
        
        self.assertEqual(user.email, playload['email'])
        self.assertEqual(user.username, playload['username'])
        self.assertTrue(user.check_password(playload['password']))
    
        
    def test_create_user_undefine_username(self):
        """ ทดสอบ function create_user ว่าได้กำหนด username มาหรือไม่"""
        playload = {
            "email": 'email@test.com',
            'password': 'password1234'
        }

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=playload['email'],
                password=playload['password'],
                username=''
            )

