from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

from PIL import Image

#MODELS HERE

class User(AbstractBaseUser, PermissionsMixin):
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('A', 'another'),
    )
    
    username = models.CharField(("username"), max_length=50, unique= True)
    email = models.EmailField(("email"), max_length=254, unique = True)
    name = models.CharField(("name"), max_length=50,blank = True)
    surname= models.CharField(("surname"), max_length=50,blank = True)
    gender = models.CharField(("gender"), max_length=1, blank = True, choices = GENDER_CHOICES)
    avatar = models.ImageField(("Avatar"),blank= True, upload_to='media/users/avatar' )
    codregistration = models.CharField(max_length=6, blank = True)
    #
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    
    
    USERNAME_FIELD = 'username'
    
    REQUIRED_FIELDS = ['email']
    
    objects = UserManager()
    
    def image_optimazer (sender, instance, **kwargs):
        print ("=================")
        if instance.avatar:
            avatar = Image.open(instance.front_page.path)
            avatar.save(instance.front_page.path, quality = 20 , optimize= True)
        
    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.name + '-' + self.surname
    