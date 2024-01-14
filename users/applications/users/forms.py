from django import forms
from django.contrib.auth import authenticate

from .models import User

class UserRegisterForm(forms.ModelForm):
    
    password1 = forms.CharField(
        label= 'Password',
        required= True,
        widget= forms.PasswordInput(
            attrs = {
                'placeholder': 'password'
            }
        )
    )
    
    password2 = forms.CharField(
        label= 'Password',
        required= True,
        widget= forms.PasswordInput(
            attrs = {
                'placeholder': 'repeat password'
            }
        )
    )
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'name',
            'surname',
            'gender',
        )
        
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            return self.add_error('password2', 'passwords do not match')
        
    def clean_password2(self):
        if len(self.cleaned_data['password1']) < 5 :
            return self.add_error('password1', 'The password must be at least 5 characters long')

class LoginForm(forms.Form):
    username = forms.CharField(
        label= 'username',
        required= True,
        widget= forms.TextInput(
            attrs = {
                'placeholder': 'username',
                'style' : '{margin: 10px}'
            }
        )
    )
    password = forms.CharField(
        label= 'Password',
        required= True,
        widget= forms.PasswordInput(
            attrs = {
                'placeholder': 'password'
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        
        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Your details are not correct')
        
class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(
        label= 'Curret Password',
        required= True,
        widget= forms.PasswordInput(
            attrs = {
                'placeholder': 'Current Password'
            }
        )
    )
    password2 = forms.CharField(
        label= 'New Password',
        required= True,
        widget= forms.PasswordInput(
            attrs = {
                'placeholder': 'New password'
            }
        )
    )

class VerificationForm(forms.Form):
    codregistration = forms.CharField(max_length=6, required=True)
    
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)
    
    
    def clean_codregistration(self):
        code = self.cleaned_data['codregistration']
        
        if len(code) == 6:
            #id and code validation
            active = User.objects.code_validation(
                self.id_user,
                code
            )
            if not active:
                raise forms.ValidationError('Your details are not correct')
        else:
            raise forms.ValidationError('Your details are not correct')
            
        
