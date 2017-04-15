from django.conf.urls import url

from Web.Home import views

urlpatterns = [
    url(r'^$', views.homePageView, name='Home'),
    url(r'^how_to_join_us$', views.howToJoinUs, name='how_to_join_us'),
    url(r'administration$', views.adminLogin, name='admin_login'),
    url(r'administration/admin_panel$', views.adminPanel, name='admin_panel'),
    url(r'administration/admin_panel/users_list$', views.validUserList, name='panel_user_list'),
    url(r'administration/admin_panel/new_admin_user$', views.registerAdminUserView, name='panel_new_user'),
    url(r'administration/admin_panel/car_list$', views.validCarList, name='panel_car_list'),
    url(r'administration/admin_panel/send_email$', views.sendEmail, name='panel_send_email'),
    url(r'administration/admin_panel/university_list$', views.universityList, name='panel_university_list'),
    url(r'administration/admin_panel/campus_list$', views.campusList, name='panel_campus_list'),
    url(r'administration/admin_panel/major_list$', views.majorsList, name='panel_major_list'),

    # WEB SERVICES
    url(r'administration/change_user_status/$', views.changeValidateStatus),
    url(r'administration/change_car_status/$', views.changeCarValidateStatus),
    url(r'administration/get_campus_from_university/$', views.getCampusFromUniversity),
    url(r'administration/get_majors_from_university/$', views.getMajorsFromUniversity),
    url(r'administration/add_university/$', views.addUniversity),
    url(r'administration/add_campus/$', views.addCampus),
    url(r'administration/add_major/$', views.addMajor),

    # DELETE WEB SERVICES
    # USERS
    url(r'administration/delete_user/$', views.deleteUser),

    # UNIVERSITYS
    url(r'administration/delete_university/$', views.deleteUniversity),
    url(r'administration/delete_campus/$', views.deleteCampus),
    url(r'administration/delete_major/$', views.deleteMajor),
]
