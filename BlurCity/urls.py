from django.conf.urls import include, url
from django.contrib import admin

from Web import Authentication
from Web.Authentication import urls
from Web import Home
from Web.Home import urls
from Web import Register
from Web.Register import urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'BlurCity.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^api/', include(Authentication.urls)),
    url(r'^', include(Home.urls, namespace='Home')),
    url(r'^register/', include(Register.urls, namespace='Register')),
    url(r'authentication/', include(Authentication.urls, namespace='Authentication'))
]
