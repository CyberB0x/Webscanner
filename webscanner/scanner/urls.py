# scanner/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('scan/<int:pk>/', views.scan, name='scan'),
    path('report/<int:pk>/', views.report, name='report'),
    path('pdf/<int:target_id>/', views.export_pdf, name='export_pdf'),

]
