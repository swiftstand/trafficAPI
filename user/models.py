from re import T
from django.db import models
from django.contrib.auth.models  import AbstractBaseUser,BaseUserManager,AbstractUser
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models.expressions import F
from django.utils import timezone
# Create your models and modelManagers here.

class CustomUserManager(BaseUserManager):
	""" This is the custom manager for model user class"""
	def create_user(self,username,is_admin,is_staff,is_superuser,password=None):
		if not username:
			raise ValueError("Users must have a Username")
		user = self.model(
											username=username,
											is_admin=True,
											is_staff=True,
										is_superuser=True)
			
		user.set_password(password)
		user.save(using=self.db)
		return user
			
	def create_superuser(self, username, password):
		user=self.create_user(
                                username=username,
                                is_admin=True,
                                is_staff=True,
                                is_superuser=True,
                                password=password,
                               )


class User(AbstractBaseUser):
    """ Custom User inheriting from AbstractBaseUser class"""

    email = models.EmailField(verbose_name='email', max_length=100)

    username = models.CharField(
                                  help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',unique=True,
                                  validators=[UnicodeUsernameValidator()], verbose_name='username', editable=True, max_length=100000
                               )

    date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)
    
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    resetter = models.CharField(max_length=12,editable=False,null=True,blank=True)
    fullname= models.CharField(default='swift only', blank =False, null=False, max_length= 100)
    is_verified = models.BooleanField(default=False)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.fullname


    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label ):
        return True

    def save(self,*args, **kwargs):
        super().save()



