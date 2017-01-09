from django.conf.urls import url

from Web.Panel import views

urlpatterns = [
    url(r'^$', views.panelView, name='Panel'),
    url(r'^car_list/$', views.carListView, name='CarList')
]