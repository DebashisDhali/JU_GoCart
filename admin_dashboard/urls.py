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
    
    # GoCarts
    path('gocarts/', views.admin_gocart_list, name='admin_gocart_list'),
    path('gocarts/add/', views.admin_add_gocart, name='admin_add_gocart'),
    path('gocarts/<int:gocart_id>/edit/', views.admin_edit_gocart, name='admin_edit_gocart'),
    path('gocarts/<int:gocart_id>/delete/', views.admin_delete_gocart, name='admin_delete_gocart'),

    # Routes
    path('routes/', views.admin_route_list, name='admin_route_list'),
    path('routes/add/', views.admin_add_route, name='admin_add_route'),
    path('routes/<int:route_id>/edit/', views.admin_edit_route, name='admin_edit_route'),
    path('routes/<int:route_id>/delete/', views.admin_delete_route, name='admin_delete_route'),

    # Stops
    path('stops/', views.admin_stop_list, name='admin_stop_list'),
    path('stops/add/', views.admin_add_stop, name='admin_add_stop'),
    path('stops/<int:stop_id>/edit/', views.admin_edit_stop, name='admin_edit_stop'),
    path('stops/<int:stop_id>/delete/', views.admin_delete_stop, name='admin_delete_stop'),

    # Schedules
    path('schedules/', views.admin_schedule_list, name='admin_schedule_list'),
    path('schedules/add/', views.admin_add_schedule, name='admin_add_schedule'),
    path('schedules/<int:schedule_id>/edit/', views.admin_edit_schedule, name='admin_edit_schedule'),
    path('schedules/<int:schedule_id>/delete/', views.admin_delete_schedule, name='admin_delete_schedule'),

    # Bookings
    path('bookings/', views.admin_booking_list, name='admin_booking_list'),
    path('bookings/<int:booking_id>/edit/', views.admin_edit_booking, name='admin_edit_booking'),
    path('bookings/<int:booking_id>/delete/', views.admin_delete_booking, name='admin_delete_booking'),

    # Contact Messages
    path('contact-messages/', views.admin_contact_messages, name='admin_contact_messages'),
    path('contact-messages/<int:message_id>/view/', views.admin_contact_view, name='admin_contact_view'),
    path('contact-messages/<int:message_id>/reply/', views.admin_contact_reply, name='admin_contact_reply'),
    path('contact-messages/<int:message_id>/delete/', views.admin_contact_delete, name='admin_contact_delete'),



]