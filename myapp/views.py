from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import TemplateView ,CreateView,FormView #
from django.contrib.auth.forms import UserCreationForm #
from django.urls import reverse_lazy #
from django.contrib.auth.views import LoginView,LogoutView, PasswordChangeView, PasswordChangeDoneView
from .forms import LoginForm,SignUpForm,UsernameChangeForm,EmailChangeForm,ImageChangeForm,Talkform
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, get_user_model,logout
from .models import CustomUser,Talk
from django.views.generic.edit import UpdateView

User = get_user_model()

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})


class UserCreateView(CreateView):
    template_name = 'user_create.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')
  

# def login_view(request):
#     return render(request, "myapp/login.html")

#ログイン機能
class AccountLogin(LoginView):
    #template_name = "myapp/login.html"
    #authentication_form = LoginForm
    #def post(self, request, *arg, **kwargs):
    form = LoginForm
    template_name = "myapp/login.html"
    """if form.is_valid():
        username = form.fields.get('username')
        user = User.objects.get(username=username)
        login(request, user)
        return render(request,"myapp/friends.html")"""
    #return render(request, 'myapp/login.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, 'myapp/login.html', {'form': form})

account_login = AccountLogin.as_view()

    
"""class Login(LoginView):
    template_name = 'login.html'
    form = LoginForm"""

@login_required()
def friends(request):
    user = request.user
    template_name = "myapp/friends.html"
    ctx = {}
    qs = CustomUser.objects.exclude(id=user.id)
    ctx["object_list"] = qs
    friends_list_1 = []
    friends_list_2 = []


    for friend in qs:
        talk = Talk.objects.filter(
        Q(message_from=user,message_to=friend ) |
        Q(message_from=friend, message_to=user)
        ).all().order_by("time").last()
        if talk :
            friends_list_1.append([user,friend,talk.talk,talk.time])
        else :
            friends_list_2.append([user,friend,"",None])
        #friends_list.append(talk)

    friends_list_1.sort(key = lambda x:x[3],reverse=True)
    friends_list = friends_list_1 + friends_list_2

    ctx["talk"] = friends_list

    return render(request, template_name, ctx)

    return render(request, "myapp/friends.html")



def talk_room(request,obj_id):
    obj = get_object_or_404(CustomUser, pk=obj_id)

    user = request.user
    template_name = "myapp/talk_room.html"
    ctx = {}
    ctx["obj"] = obj

    talk = Talk.objects.filter(
        Q(message_from=user,message_to=obj ) |
        Q(message_from=obj, message_to=user)
    ).all().order_by("time")
    ctx["talk"] = talk

    form = Talkform()

    if request.method == 'POST':
        new_talk = Talk(message_from=user, message_to=obj)
        form = Talkform(request.POST,instance=new_talk)
        ctx["form"] = form
        if form.is_valid():
            form.save()
            return redirect("talk_room", obj_id)
        else: return render(request, "myapp/friends.html")


    else:
        form = Talkform()
        ctx["form"] = form
    return render(request, template_name, ctx)


    return render(request, "myapp/talk_room.html")
@login_required()
def setting(request):
    return render(request, "myapp/setting.html")

def logout_request(request):
    logout(request)
    return redirect('index')

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    success_url = reverse_lazy('password_change_done')
    template_name = 'myapp/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context

class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    """パスワード変更完了"""
    template_name = 'myapp/password_change_done.html'




class UsernameChange(LoginRequiredMixin,FormView):
    template_name = 'myapp/username_change.html'
    form_class = UsernameChangeForm
    success_url = reverse_lazy('username_change_done')
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'username' : self.request.user.username,
        })
        return kwargs
    
class UsernameChangeDone(LoginRequiredMixin,PasswordChangeDoneView):#このformviewが悪い
    template_name = 'myapp/username_change_done.html'

class EmailChangeView(LoginRequiredMixin, FormView):
    template_name = 'myapp/email_change.html'
    form_class = EmailChangeForm
    success_url = reverse_lazy('email_change_done')
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'email' : self.request.user.email,
        })
        return kwargs
    
class EmailChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    template_name = 'myapp/email_change_done.html'

class ImageChangeView(LoginRequiredMixin, FormView):
    template_name = 'myapp/image_change.html'
    form_class = ImageChangeForm
    success_url = reverse_lazy('image_change_done')
    
    def icon(request):
        user = request.user

    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'image' : self.request.user.image,
        })
        return kwargs
        
"""class ImageChangeView(UpdateView):
    template_name = "myapp/image_change.html"
    model = CustomUser
    form = ImageChangeForm
    fields = ['image']
    #success_url = reverse_lazy('image_change_done')
    def get_success_url(self):
        return reverse("myapp:image_change_done.html", kwargs={"pk":self.object.pk})"""


class ImageChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    template_name = 'myapp/image_change_done.html'