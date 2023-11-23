from django.urls import path
from . import views

app_name = 'authors'
urlpatterns = [
    path('authors/', views.authors, name='authors'),
    path('authors-admin/', views.authorsAdmin, name='authors-admin'),
    path('sending-email/', views.sendingEmail, name='sending-email')
]
