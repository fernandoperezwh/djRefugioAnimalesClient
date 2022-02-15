"""djRefugioAnimalesClient URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.views.static import serve 

# local imports
from apps.refugio_animales.views import pets_list
from djRefugioAnimalesClient import settings
from djRefugioAnimalesClient.views import oauth_callback

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^oauth/callback', oauth_callback, name='oauth_callback'),
    url(r'^app/', include('apps.refugio_animales.urls')),
    url(r'^401/$', TemplateView.as_view(template_name='errors/forbidden.html'), name='forbidden_error')
]
urlpatterns += [
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
