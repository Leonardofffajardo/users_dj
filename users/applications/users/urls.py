from django.urls import path

from . import views

app_name = "users_app"

urlpatterns = [
    path('register/', 
         views.UserRegisterView.as_view(), 
         name='register'),
    path('login/', 
         views.LoginUser.as_view(), 
         name='user-login'),
    path('logout/', 
         views.LogoutUser.as_view(), 
         name='user-logout'),
    path('updatedetails/<pk>/', 
         views.UsersUpdateView.as_view(), 
         name='update-details'),
    path('password-update/', 
         views.UpdatePasswordView.as_view(), 
         name='password-update'),
    path('user-verification/<pk>/', 
         views.CodVerificationView.as_view(), 
         name='user-verification'),
]