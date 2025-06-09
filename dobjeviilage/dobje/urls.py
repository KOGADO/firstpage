from django.contrib import admin
from django.urls import path
from dobje.views import home_view, info_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('homedobje/', info_view, name='info_view'),
]