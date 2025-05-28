from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('', views.admin_dashboard, name='admin_dashboard'),

    # Drivers
    path('drivers/', views.admin_driver_list, name='admin_driver_list'),
    path('drivers/<int:driver_id>/edit/', views.admin_edit_driver, name='admin_edit_driver'),
    path('drivers/<int:driver_id>/delete/', views.admin_delete_driver, name='admin_delete_driver'),

    # Students
    path('students/', views.admin_student_list, name='admin_student_list'),
    path('students/<int:student_id>/edit/', views.admin_edit_student, name='admin_edit_student'),
    path('students/<int:student_id>/delete/', views.admin_delete_student, name='admin_delete_student'),
]