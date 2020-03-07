from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
	def create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError("Email required")
		if not password:
			raise ValuError("Password required")

		user=self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self,email, password):
		user=self.create_user(email,password)
		user.is_staff=True
		user.is_superuser=True
		user.is_admin=True
		user.save()
		return user

class User(AbstractBaseUser, PermissionsMixin):
	GENDER=[('M','M'),('F','F')]
	email= models.EmailField(unique=True)
	username=models.CharField(max_length=200,null=False,blank=False)
	age= models.IntegerField(blank=False, null=False, default=0)
	gender= models.CharField(choices= GENDER, max_length=15)
	is_therapist=models.BooleanField(default=False)
	date_joined = models.DateTimeField(auto_now_add=True)
	is_staff= models.BooleanField(default=False)
	is_active= models.BooleanField(default=True)
	is_superuser= models.BooleanField(default=False)
	is_admin=models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

class Patient(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	pic=models.ImageField(upload_to='patient_pic',null=True,blank=True)
	phone_regex=RegexValidator(regex = r'^\+?1?\d{9,10}$' ,message='Phone number must be valid')
	phone= models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True, default=None)
	Address=models.TextField()
	twitter_address=models.URLField()
	is_therapist=False

	def __str__(self):
		return self.user.username

class Therapist(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	pic=models.ImageField(upload_to='patient_pic',null=True,blank=True)
	phone_regex=RegexValidator(regex = r'^\+?1?\d{9,10}$' ,message='Phone number must be valid')
	phone= models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True, default=None)
	Address=models.TextField()
	user.is_therapist=True

	def __str__(self):
		return self.user.username



class  Educ(models.Model):
	title=models.CharField(max_length=255)
	description=models.TextField()
	certificate=models.FileField(upload_to='filer/')
	therapist=models.ForeignKey(Therapist,on_delete=models.CASCADE)
	def __str__(self):
		return self.title

	def summary(self):
		return self.body[:100]
