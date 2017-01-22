from django.conf.urls import url

from Web.Panel import views

urlpatterns = [
    url(r'^$', views.panelView, name='Panel'),
    url(r'^car_list/$', views.carListView, name='CarList'),
    url(r'^route_list/$', views.routeListView, name='RouteList'),
    url(r'^route/(?P<route_pk>[0-9]+)/$', views.routeView, name='Route'),
    url(r'^notifications/$', views.notificationView, name='Notifications'),

    # WEB SERVICES
    url(r'^save_route/$', views.saveRouteService),
    url(r'^update_route/$', views.updateRouteService),
    url(r'^save_markers/$', views.saveRouteMarkers),
    url(r'^update_markers/$', views.updateRouteMarkers),
    url(r'^make_notification/$', views.makeNotification),
    url(r'^update_notification/$', views.updateNotification),
]