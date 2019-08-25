from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views


app_name = 'profiles'

urlpatterns = [
    path('register/',views.register_view, name='register'),
    path('update/',views.update_view, name='update'),
    path('update/password',views.update_password_view, name='update_pass'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    ]