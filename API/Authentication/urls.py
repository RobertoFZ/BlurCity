from django.conf.urls import url

from API.Authentication import views

urlpatterns = [
    url(r'new_user/', views.register_user)
]
