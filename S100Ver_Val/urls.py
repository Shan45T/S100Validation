"""S100Ver_Val URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from file_reading.api import router
from validation.api import router_validation
from file_reading.views import S100READINGFILE
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('Login', S100READINGFILE.Login, name='Login'),
    path('signup', S100READINGFILE.signup, name='signup'),
    path('changepassword', S100READINGFILE.changepassword, name='changepassword'),
    path('', include(router.urls)),
    path('', include(router_validation.urls)),
    path('admin/', admin.site.urls),
    path('home', S100READINGFILE.home, name='home'),
    #path('swagger', schema_view),
    path('api-token-auth', obtain_auth_token, name='api_token_auth'),     


]
