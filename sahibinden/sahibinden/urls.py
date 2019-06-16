"""sahibinden URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include, reverse
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include('ad_messages.urls')),    #This will be changed when the main app created.
    path('admin/', admin.site.urls),
    path('ad_messages/', include('ad_messages.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_reset'),
    path('oauth/', include('social_django.urls', namespace='social')),
   
]
