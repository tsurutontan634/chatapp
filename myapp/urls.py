from django.urls import path,include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import UserCreateView
from django.contrib.auth import logout#

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.AccountLogin.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('<int:obj_id>/', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('accounts/', include('django.contrib.auth.urls')),# これを追加
    path('logout/',views.logout_request,name='logout'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'), #追加
    path('password_change_done/', views.PasswordChangeDone.as_view(), name='password_change_done'), #追加
    path('email_change/', views.EmailChangeView.as_view(), name='email_change'), #追加
    path('email_change_done/', views.EmailChangeDone.as_view(), name='email_change_done'), #追加
    path('username_change/', views.UsernameChange.as_view(), name='username_change'), #追加
    path('username_change_done/', views.UsernameChangeDone.as_view(), name='username_change_done'), #追加
    path('image_change/', views.ImageChangeView.as_view(), name='image_change'), #追加
    path('image_change_done/', views.ImageChangeDone.as_view(), name='image_change_done'), #追加
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)