from django.conf.urls import url

from Web.Register import views

urlpatterns = [
    url(r'user/$', views.registerUserView, name='RegisterUser'),
    url(r'car/$', views.registerCarView, name='RegisterCar'),
    url(r'route/$', views.registerRoute, name='RegisterRoute'),

    url(r'car=(?P<car_pk>[0-9]+)/update/$', views.editCarView, name='EditCar'),
]
