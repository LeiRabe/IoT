from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#Création du "manager" des objets de la class User
class MyUserManager(BaseUserManager):
    #fonction permettant de créer un user
    def create_user(self, email, username,firstname,lastname,gender,last_login,qrcode,status,password):
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
                status=status,
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                qrcode=qrcode,
                username=username,
                password=password,
                last_login=last_login,
        )

        user.set_password(password)
        user.save(using=self._db)    #sauvegare du user dans la bdd
        return user

    #fonction permettant de créer un admin/prof
    def create_superuser(self, id, email, username,firstname,lastname,gender, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
                status="professeur",
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                username=username,
        )

        return user

class MyAccessManager():
    def create_access(self,idUser,idPortique,dateAccess ):
        
        #Manager de la class Accès
        access = self.model(
                idUser = idUser,
                idPortique = idPortique,
                dateAccess = dateAccess,
        )

        access.save(using=self._db)
        return access        


#Création de la classe user pour enrichir la bdd
class User(AbstractBaseUser):
    class Meta:
      db_table = 'User'
    
    idUser                  = models.AutoField(primary_key=True)
    username                = models.CharField(max_length=60, unique=True)
    firstname               = models.CharField(max_length=70, unique=False)
    lastname                = models.CharField(max_length=50, unique=False)
    email                   = models.EmailField(verbose_name="email",max_length=50, unique=True)
    gender                  = models.CharField(max_length=2)
    status                  = models.CharField(max_length=50)
    qrcode                  = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = 'email'  #Le paramètre qui fait office d'identifiant lors de la connection
    REQUIRED_FIELDS = ['username','firstname','lastname','gender','status','qrcode',]   #Les paramètres requis pour la création d'un user avec un form
    
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True
# Create your models here.

#Classe accès pour enrichir la bdd avec les accès aux portiques
class Access(models.Model): 
    class Meta:
      db_table = 'Access'
    idAccess                 = models.AutoField(primary_key=True)
    idUser                = models.IntegerField()
    idPortique               = models.IntegerField(max_length=70, unique=False)
    dateAccess                = models.DateField(max_length=50, unique=False)

    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True