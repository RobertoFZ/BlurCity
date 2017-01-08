from django.conf.urls import url

from Web.Home import views

urlpatterns = [
    url(r'^$', views.homePageView, name='Home')
]
