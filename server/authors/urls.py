from django.urls import path
from . import views

app_name = 'authors'
urlpatterns = [
    path('authors/', views.authors, name='authors'),
    path('sending-email/', views.sendingEmail, name='sending-email')
]
