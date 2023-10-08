from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views import DownloadPdf

urlpatterns = [
    path('', views.index, name='index'),
    path('pdf/', DownloadPdf), 
    path(r'favicon\.ico', RedirectView.as_view(url='/static/images/fav.png')),
]