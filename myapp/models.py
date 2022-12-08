from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    
    def create_user(self, email, username, password=None):#ユーザーのフィールドを作成
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            ##image = models.ImageField(null=True, blank=True,upload_to= 'image/' ,default="")
            #is_active = models.BooleanField(default=True)
            #date_of_birth=date_of_birth,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,  username, password=None):#管理ユーザーのフィールドを作成
        user = self.create_user(
            email=email,
            #image = models.ImageField(null=True, blank=True,upload_to= 'myapp/media_local'),
            password=password,
            username=username,
            #image=""
            #nickname=nickname,
            #date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
        #REQUIRED_FIELDS = ['username', 'email', 'password',]

class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Username',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=150,unique=True)
    image = models.ImageField(null=True, blank=True,upload_to= 'image/',default="")
    #is_active = models.BooleanField(default=True)
    #is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):#Trueを返して、権限があることを知らせる
        return True

    def has_module_perms(self, app_label):#Trueを返して、アプリ（App）のモデル（Model）へ接続できるようにする
        return True

    #@property
    def is_staff(self):#Trueの場合、Django管理サイトにログインできる
        return self.is_staff


class Talk(models.Model):
    talk =  models.CharField(max_length=300)
    time =  models.DateTimeField(auto_now_add=True)
    #message_from = models.CharField(max_length=300,)
    #message_to = models.CharField(max_length=300,)
    message_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="message_from")
    message_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="message_to")
    def __str__(self):
        return str(self.talk)