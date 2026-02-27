from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class CustomUserManager(BaseUserManager):

    #custom user manager

    def create_user(self,email,password=None, **extra_fields):

      
        if not email:
            raise ValueError("username needed")
        if not password:
            raise ValueError("password is needed")
       
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email , password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("is staff must be true"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("the user must be super user"))
  
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):

     
    # custom user that username field is email

    email = models.EmailField(_('email'),unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    is_verified=models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects=CustomUserManager()

    def __str__(self):
        return self.email

class Province(models.Model):
    name=models.CharField(_("name"))

class City(models.Model):
    name=models.CharField(_("name"))
    province=models.ForeignKey(Province,verbose_name=_("province"),on_delete=models.CASCADE,related_name='city') 

class UserProfile(models.Model):

    user=models.OneToOneField(CustomUser,verbose_name=_("user"),on_delete=models.CASCADE,related_name='profile')
    first_name=models.CharField(_("first name"),max_length=25,null=True,blank=True)
    last_name=models.CharField(_("last name"),max_length=30,null=True,blank=True)
    address=models.TextField(_('adrress'),null=True,blank=True)
    postal_code=models.CharField(_("postal code"))
    city=models.ForeignKey(City,verbose_name=_("city"),on_delete=models.SET_NULL,related_name="profile",null=True)
    province=models.ForeignKey(Province,verbose_name=_("province"),on_delete=models.SET_NULL,related_name='profile',null=True)
    plaque=models.IntegerField(_("plaque"),null=True)


@receiver(post_save,sender=CustomUser)
def create_profile(sender,instance,created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    