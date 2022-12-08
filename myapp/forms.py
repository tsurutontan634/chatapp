#from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import Talk
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       #htmlの表示を変更可能にします
       self.fields['username'].widget.attrs['class'] = 'form-control'
       self.fields['password'].widget.attrs['class'] = 'form-control'
       class Meta:
           model=User
           fields=("username","password1")

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()
# ユーザ作成フォームを継承
class SignUpForm(UserCreationForm):
    username = forms.CharField(label="ユーザー名")
    email = forms.EmailField(label="メールアドレス")
    image = forms.ImageField(label="画像")
    password1 = forms.CharField(widget=forms.PasswordInput ,label="パスワード")
    password2 = forms.CharField(widget=forms.PasswordInput ,label="パスワード確認用")

    class Meta:
        model = User
        fields=("username","email","image")


#---------

 



class UsernameChangeForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
        ]

    def __init__(self,username=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        if username:
            self.fields['username'].widget.attrs['value'] = username
 
    def update(self, user):
        user.username = self.cleaned_data['username']
        user.save()

class EmailChangeForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
        ]

    def __init__(self,email=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        if email:
            self.fields['email'].widget.attrs['value'] = email
 
    def update(self, user):
        user.email = self.cleaned_data['email']
        user.save()

class ImageChangeForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'image',
        ]

    def __init__(self,image=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        if image:
            self.fields['image'].widget.attrs['value'] = image
 
    def update(self, user):
        user.image = self.cleaned_data['image']
        user.save()





"""class ImageChangeForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'image',
        ]

    def __init__(self,image=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        if image:
            self.fields['image'].widget.attrs['value'] = image
 
    def update(self, user):
        user.image = self.cleaned_data['image']
        user.save()"""



class Talkform(ModelForm):
    class Meta:
        model = Talk
        fields = [
            'talk',
        ]
        