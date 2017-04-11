from django.conf.urls import url

from Web.Home import views

urlpatterns = [
    url(r'^$', views.homePageView, name='Home'),
    url(r'administration$', views.validUserList, name='valid_users'),

    # WEB SERVICES
    url(r'administration/change_user_status/$', views.changeValidateStatus),
    url(r'administration/add_university/$', views.addUniversity),
    url(r'administration/add_campus/$', views.addCampus),
    url(r'administration/add_major/$', views.addMajor),

    # DELETE WEB SERVICES
    url(r'administration/delete_university/$', views.deleteUniversity),
    url(r'administration/delete_campus/$', views.deleteCampus),
    url(r'administration/delete_major/$', views.deleteMajor),
]
