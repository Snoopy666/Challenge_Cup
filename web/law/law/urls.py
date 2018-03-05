from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from front import views
urlpatterns = [
    url('^$', views.index),
    url('^login$', views.login),
    url('^change$', views.changeCrit),
    url('^quit$', views.quit),
    url('^save$', views.save)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)