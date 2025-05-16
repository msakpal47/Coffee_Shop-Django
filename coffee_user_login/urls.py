from django.urls import path
from coffee_user_login import views

app_name = 'coffee_user_login'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]