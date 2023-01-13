from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, email, username,firstname,lastname,gender,status='eleve', password=None, qrcode):
        if not email:
            raise ValueError("Users must have an email adress")
        if not username:
            raise ValueError("Users must have a username")
        if not firstname:
            raise ValueError("Users must have a firstname")
        if not lastname:
            raise ValueError("Users must have a lastname")
        if not gender:
            raise ValueError("Users must have a gender")

        user = self.model(
                email=self.normalize_email(email),
                status="eleve",
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                username=username,
                qrcode=qrcode,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, username,firstname,lastname,gender, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
                status="professeur",
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                username=username,
        )

        return user

        



class User(AbstractBaseUser):
    class Meta:
      db_table = 'User'
    
    id                      = models.AutoField(primary_key=True)
    username                = models.CharField(max_length=50, unique=True)
    firstname               = models.CharField(max_length=50, unique=False)
    lastname                = models.CharField(max_length=50, unique=False)
    email                   = models.EmailField(verbose_name="email",max_length=50, unique=True)
    gender                  = models.CharField(max_length=2)
    status                  = models.CharField(max_length=2)
    qrcode                  = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','firstname','lastname','gender','qrcode',]

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True
# Create your models here.
