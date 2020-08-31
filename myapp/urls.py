from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('signup', views.signup, name='signup'),
    path('signup', SignUp.as_view(), , name='signup'),
    path('login', views.login, name='login'),
    path('friends', views.friends, name='friends'),
    path('talk_room', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
]