from typing import Any
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.views.generic import (
    CreateView,View, UpdateView
)
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import (
    FormView,
)
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import UserRegisterForm, LoginForm, UpdatePasswordForm, VerificationForm
from .models import User
from .funtions import code_generator

class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'
    
    def form_valid(self, form):
        
        # generated code
        random_code = code_generator()
        
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            name = form.cleaned_data['name'],
            surname = form.cleaned_data['surname'],
            gender = form.cleaned_data['gender'],
            #codregistration = random_code
        )
        
        #send code to user email
        affair = 'Email confirmation'
        message = 'verification code: ' + random_code
        sender_email = 'leo.fajardo072004@gmail.com'
        #
        send_mail(affair, message, sender_email, [form.cleaned_data['email'],])
        #redirect to validation screen
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                kwargs= {'pk': usuario.id}
            )
        )
        return super(UserRegisterView, self).form_valid(form)
    
class LoginUser(FormView):
    template_name = 'users/login.html' 
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')
    
    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)
    
class LogoutUser(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )

class UsersUpdateView(LoginRequiredMixin, UpdateView):
            
    template_name = "users/updateusers.html"
    model = User
    fields = [
        'username',
        'email',
        'name',
        'surname',
        'gender',
    ]
    success_url = reverse_lazy ('home_app:panel')
    login_url = reverse_lazy('users_app:user-login')
    
    def post(self,request,*args,**kwargs):
        self.object = self.get_object
        return super().post(request,*args,**kwargs)

class UpdatePasswordView(LoginRequiredMixin,FormView):
    template_name = 'users/password_update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')
    
    def form_valid(self, form):
        userv = self.request.user
        user = authenticate(
            username = userv.username,
            password=form.cleaned_data['password1'],
        )
        
        if user:
            new_password = form.cleaned_data['password2']
            userv.set_password(new_password)
            userv.save()
            
        logout(self.request)
        
        return super(UpdatePasswordView, self).form_valid(form)

class CodVerificationView(FormView):
    template_name = 'users/verification.html' 
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user-login')
    
    def get_form_kwargs(self):
        kwargs = super(CodVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk' : self.kwargs ['pk']
        })
        return kwargs
    
    def form_valid(self, form):
        
        User.objects.filter(
            id = self.kwargs['pk']
        ).update(
            is_active = True
        )
        return super(CodVerificationView, self).form_valid(form)