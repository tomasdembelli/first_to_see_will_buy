from django.urls import path, re_path
from . import views

app_name = 'ad_messages'    # namespacing to differentiate that urls from other apps in templates
urlpatterns = [
    path('', views.index, name='index'),
    path('ad_list/', views.ad_list, name='ad_list'),
    #path('ads/<int:ad_id_title>/', views.detail, name='detail'),
    path('ad_detail/<int:ad_id>/', views.ad_detail, name='detail'),
    path('ad_create/', views.ad_create, name='ad_create'),
    path('ad_update/<int:ad_id>/', views.ad_update, name='ad_update'),
    path('my_ads/', views.my_ads, name='my_ads'),
    path('my_favourites/', views.my_favourites, name='my_favourites'),
    path('register_user/', views.register_user, name='register_user'),
    path('signup/', views.signup, name='signup'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z\_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]

