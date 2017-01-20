from django.conf.urls import url

from Web.Panel import views

urlpatterns = [
    url(r'^$', views.panelView, name='Panel'),
    url(r'^car_list/$', views.carListView, name='CarList'),

    # WEB SERVICES
    url(r'^save_route/$', views.saveRouteService),
    url(r'^save_days/$', views.saveRouteDays),
    url(r'^save_markers/$', views.saveRouteMarkers),
]