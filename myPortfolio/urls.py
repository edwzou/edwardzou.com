from django.contrib import admin
from django.urls import path,include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cvapp.urls')),
    path(r'favicon\.ico', RedirectView.as_view(url='/static/images/favico.ico')),
]
