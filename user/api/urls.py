from django.urls import path,include
from user.api import views as user_api_views
from rest_framework.authtoken.views import obtain_auth_token
app_name = 'user'

urlpatterns = [
    path('register/', user_api_views.Register, name="register"),
    path('logout/', user_api_views.Logout, name="logout"),
    path('login/', user_api_views.login, name="login"),
    path('password/reset/', user_api_views.forgotpassword, name='forgot'),
    path('password/confirm/', user_api_views.confirm_reset, name='confirm')
] 