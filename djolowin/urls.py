"""djolowin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

urlpatterns = [
    path('', include('base.urls', namespace='base')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('auction/', include('auction.urls', namespace='auction')),
    path("bundle/", include("bundle.urls", namespace="bundle")),
    path('collection/', include('collection.urls', namespace='collection')),
    path('currency/', include('app_currency.urls', namespace='currency')),
    path('playercard/', include('playercard.urls', namespace='playercard')),
    path('transaction/', include('transaction.urls', namespace='transaction')),
    path('wallet/', include('wallet.urls', namespace='wallet')),
]
