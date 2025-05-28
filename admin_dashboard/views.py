from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

from .decorators import admin_login_required
from .forms import GoCartForm

from gocart.models import (
    GoCart, User, Route, Stop, Schedule,
    SeatLayout, Booking, ContactMessage
)

# Admin authentication
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or not an admin user.")
    
    return render(request, 'admin_dashboard/admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# Dashboard view
@admin_login_required
def admin_dashboard(request):
    context = {
        'gocart_count': GoCart.objects.count(),
        'route_count': Route.objects.count(),
        'stop_count': Stop.objects.count(),
        'driver_count': User.objects.filter(role='driver').count(),
        'student_count': User.objects.filter(role='student').count(),
        'schedule_count': Schedule.objects.count(),
        'booking_count': Booking.objects.count(),
        'contact_message_count': ContactMessage.objects.count(),
    }
    return render(request, 'admin_dashboard/admin_dashboard.html', context)

# Drivers
@admin_login_required
def admin_driver_list(request):
    drivers = User.objects.filter(role='driver')
    return render(request, 'admin_dashboard/admin_driver_list.html', {'drivers': drivers})

@admin_login_required
def admin_edit_driver(request, driver_id):
    driver = get_object_or_404(User, id=driver_id, role='driver')
    if request.method == 'POST':
        driver.first_name = request.POST.get('first_name')
        driver.last_name = request.POST.get('last_name')
        driver.email = request.POST.get('email')
        driver.phone = request.POST.get('phone')
        driver.gender = request.POST.get('gender')
        driver.dob = request.POST.get('dob') or None
        driver.present_address = request.POST.get('present_address')
        driver.postal_code = request.POST.get('postal_code')
        driver.home_district = request.POST.get('home_district')
        driver.nationality = request.POST.get('nationality')
        driver.nid_card_no = request.POST.get('nid_card_no')

        if 'profile_picture' in request.FILES:
            driver.profile_picture = request.FILES['profile_picture']

        driver.save()
        messages.success(request, "Driver updated successfully.")
        return redirect('admin_driver_list')
    return render(request, 'admin_dashboard/admin_edit_driver.html', {'driver': driver})


@admin_login_required
def admin_delete_driver(request, driver_id):
    driver = get_object_or_404(User, id=driver_id, role='driver')
    if request.method == 'POST':
        driver.delete()
        messages.success(request, "Driver deleted successfully.")
        return redirect('admin_driver_list')
    return redirect('admin_driver_list')

# Students
@admin_login_required
def admin_student_list(request):
    students = User.objects.filter(role='student')
    return render(request, 'admin_dashboard/admin_student_list.html', {'students': students})

@admin_login_required
def admin_edit_student(request, student_id):
    student = get_object_or_404(User, id=student_id, role='student')
    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.gender = request.POST.get('gender')
        student.dob = request.POST.get('dob') or None
        student.present_address = request.POST.get('present_address')
        student.postal_code = request.POST.get('postal_code')
        student.home_district = request.POST.get('home_district')
        student.nationality = request.POST.get('nationality')

        if 'profile_picture' in request.FILES:
            student.profile_picture = request.FILES['profile_picture']

        student.save()
        messages.success(request, "Student updated successfully.")
        return redirect('admin_student_list')

    return render(request, 'admin_dashboard/admin_edit_student.html', {'student': student})

@admin_login_required
def admin_delete_student(request, student_id):
    student = get_object_or_404(User, id=student_id, role='student')
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect('admin_student_list')
    return redirect('admin_student_list')
