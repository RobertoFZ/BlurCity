from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^choice_login_type', views.choiceLoginTypeView, name='ChoiceLogin'),
    url(r'^login$', views.loginView, name='Login'),
    url(r'^logout_user$', views.logoutUser, name='LogoutUser'),
]
