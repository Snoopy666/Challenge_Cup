from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from front import views
from django.contrib import admin

urlpatterns = [
    url('^$', views.index),
    url('^login$', views.login),
    url('^change$', views.changeCrit),
    url('^quit$', views.quit),
    url('^save$', views.save),
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)