from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save
from notifications.signals import notify

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, username=None,email=None , password=None):
        """
        Creates and saves a User with the given email, username and password.
        """
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,email, password):
        """
        Creates and saves a superuser with the given email,username and password.
        """
        user = self.create_user(
            
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(
        verbose_name='user name',
        max_length=255,
        unique=True,
    )
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    first_name = models.CharField(
            max_length=120,
            null=True,
            blank=True)
            
    last_name = models.CharField(
            max_length=120,
            null=True,
            blank=True)
            
    is_member = models.BooleanField(default=False, verbose_name='Is Paid Member')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return "%s %s" %(self.first_name,self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return self.email
        
    def __unicode__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class UserProfile(models.Model):
    user = models.OneToOneField(MyUser)
    bio = models.TextField(null=True, blank=True)
    
    facebook_link=models.CharField(max_length=320, 
            null=True, 
            blank=True,
            verbose_name="Facebook profile url")
    
    def __unicode__(self):
        return self.user.username
        
    def __str__(self):
        return self.user.username
        
def new_user_receiver(sender,instance,created,*args, **kwargs):
    if created:
        new_profile, is_created = UserProfile.objects.get_or_create(user=instance)
        print new_profile, is_created
        notify.send(instance, 
                    recipient=MyUser.objects.get(username="climberwb"),
                    verb="New User created")
        #
        # merchant account customer id -- stripe vs braintree
        # sendd email for verifying user email
    
post_save.connect(new_user_receiver, sender=MyUser)