"""Dissertation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from . import scanner
# from . import baseview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('home/', views.home,name='home'),
    path('audit/', views.audit,name='audit'),

    path('scanner/', scanner.scanner,name='scanner'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('home/', baseview.home,name='home'),
    # path('login/', views.login,name='login'),
    path('devicelogin/<ip>/<type>/<ios>', views.devicelogin,name='devicelogin'),
    path('device/', views.device,name='device'),
    path('switch/', views.switch,name='switch'),
    path('sshlogin/', views.sshLogin,name='sshLogin'),
    path('confChange/', views.confChange,name='confChange'),
    path('junoconfChange/', views.junoconfChange,name='junoconfChange'),
    path('backupConf/', views.backupConf,name='backupConf'),
    path('swconfChange/', views.swconfChange,name='swconfChange'),


]
