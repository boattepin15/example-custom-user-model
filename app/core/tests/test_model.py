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
        with self.assertRaises(ValueError) as context:
            get_user_model().objects.create_user(
                email=playload['email'],
                password=playload['password'],
                username=''
            )
        self.assertEqual(str(context.exception), 'The given username must be set')
    


    def test_create_superuser_undefine_username(self):
        """ทดสอบการสร้าง superuser โดยไม่กำหนด username"""
        playload = {
            'email':'email@test.com',
            'password':'password1234',
            'username':''
        }
   
        with self.assertRaises(ValueError) as context:
            get_user_model().objects.create_superuser(
                email=playload['email'],
                password=playload['password'],
                username=playload['username']
            )
        self.assertEqual(str(context.exception), "The given username must be set")




    def test_create_superuser_success(self):
        """ ทดสอบ ฟังก์ชัน create_superuser สมัครแอดมิน"""
        playload = {
            'email':'email@test.com',
            'username':'admin',
            'password':'password1234'
        }

        superuser = get_user_model().objects.create_superuser(
            email=playload['email'],
            username=playload['username'],
            password=playload['password']
        )
        self.assertEqual(str(superuser), playload['username'])
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


    def test_create_superuser_without_is_staff_raises_error(self):
        """ทดสอบการสร้าง superuser โดยไม่มี is_staff จะ raise error"""
        with self.assertRaises(ValueError) as context:
            get_user_model().objects.create_superuser(
                email='superuser@test.com',
                password='superuserpass',
                username='namesuperuser',
                is_staff=False
            )
        self.assertEqual(str(context.exception), 'Superuser must have is_staff=True.')



    def test_create_superuser_without_is_superuser_raises_error(self):
        """ทดสอบการสร้าง superuser โดยไม่มี is_superuser จะ raise error"""
        with self.assertRaises(ValueError) as context:
            get_user_model().objects.create_superuser(
                email='superuser@test.com',
                password='superuserpass',
                username='namesuperuser',
                is_superuser=False
            )
        self.assertEqual(str(context.exception), 'Superuser must have is_superuser=True.')
