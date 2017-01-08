from django.conf.urls import url

from Web.Register import views

urlpatterns = [
    url(r'user/$', views.registerUserView, name='RegisterUser')
]