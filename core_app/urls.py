from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.registration_page, name='registration'),
    path('register/submit/', views.register_submit, name='register_submit'),
    path('attendance/', views.attendance_page, name='attendance'),
    path('attendance/submit/', views.attendance_submit, name='attendance_submit'),
    path('download-attendance/', views.download_attendance, name='download_attendance'),
]
