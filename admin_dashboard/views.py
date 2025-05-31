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


@admin_login_required
def admin_gocart_list(request):
    carts = GoCart.objects.select_related('driver', 'route')
    return render(request, 'admin_dashboard/admin_gocart_list.html', {'gocarts': carts})

# Add GoCart
@admin_login_required
def admin_add_gocart(request):
    if request.method == 'POST':
        form = GoCartForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "GoCart added successfully.")
            return redirect('admin_gocart_list')
    else:
        form = GoCartForm()
    return render(request, 'admin_dashboard/admin_add_gocart.html', {'form': form})

# Edit GoCart
@admin_login_required
def admin_edit_gocart(request, gocart_id):
    gocart = get_object_or_404(GoCart, id=gocart_id)
    if request.method == 'POST':
        form = GoCartForm(request.POST, instance=gocart)
        if form.is_valid():
            form.save()
            messages.success(request, "GoCart updated successfully.")
            return redirect('admin_gocart_list')
    else:
        form = GoCartForm(instance=gocart)
    return render(request, 'admin_dashboard/admin_edit_gocart.html', {'form': form, 'gocart': gocart})

# Delete GoCart
@admin_login_required
def admin_delete_gocart(request, gocart_id):
    gocart = get_object_or_404(GoCart, id=gocart_id)
    if request.method == 'POST':
        gocart.delete()
        messages.success(request, "GoCart deleted successfully.")
        return redirect('admin_gocart_list')
    return redirect('admin_gocart_list')

# Routes
@admin_login_required
def admin_route_list(request):
    routes = Route.objects.prefetch_related('stops')
    return render(request, 'admin_dashboard/admin_route_list.html', {'routes': routes})

# Add Route
@admin_login_required
def admin_add_route(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        stops = request.POST.getlist('stops')
        route = Route.objects.create(name=name)
        if stops:
            route.stops.set(stops)
        messages.success(request, "Route added successfully.")
        return redirect('admin_route_list')
    
    return render(request, 'admin_dashboard/admin_add_route.html', {
        'stops': Stop.objects.all()
    })

# Edit Route
@admin_login_required
def admin_edit_route(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    if request.method == 'POST':
        route.name = request.POST.get('name')
        stops = request.POST.getlist('stops')
        route.save()
        route.stops.set(stops)
        messages.success(request, "Route updated successfully.")
        return redirect('admin_route_list')

    return render(request, 'admin_dashboard/admin_edit_route.html', {
        'route': route,
        'stops': Stop.objects.all()
    })

# Delete Route
@admin_login_required
def admin_delete_route(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    if request.method == 'POST':
        route.delete()
        messages.success(request, "Route deleted successfully.")
        return redirect('admin_route_list')
    return redirect('admin_route_list')

# Stops
@admin_login_required
def admin_stop_list(request):
    stops = Stop.objects.all()
    return render(request, 'admin_dashboard/admin_stop_list.html', {'stops': stops})

# Add Stop
@admin_login_required
def admin_add_stop(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        if name and lat and lng:
            Stop.objects.create(name=name, lat=lat, lng=lng)
            messages.success(request, 'Stop added successfully.')
            return redirect('admin_stop_list')
    return render(request, 'admin_dashboard/admin_add_stop.html')

# Edit Stop
@admin_login_required
def admin_edit_stop(request, stop_id):
    stop = get_object_or_404(Stop, id=stop_id)
    if request.method == 'POST':
        stop.name = request.POST.get('name')
        stop.lat = request.POST.get('lat')
        stop.lng = request.POST.get('lng')
        stop.save()
        messages.success(request, 'Stop updated successfully.')
        return redirect('admin_stop_list')
    return render(request, 'admin_dashboard/admin_edit_stop.html', {'stop': stop})

# Delete Stop
@admin_login_required
def admin_delete_stop(request, stop_id):    
    stop = get_object_or_404(Stop, id=stop_id)
    if request.method == 'POST':
        stop.delete()
        messages.success(request, 'Stop deleted successfully.')
        return redirect('admin_stop_list')
    return redirect('admin_stop_list')

# Schedules
@admin_login_required
def admin_schedule_list(request):
    schedules = Schedule.objects.select_related('cart')
    return render(request, 'admin_dashboard/admin_schedule_list.html', {'schedules': schedules})

# Add Schedule
@admin_login_required
def admin_add_schedule(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart')
        travel_date = request.POST.get('travel_date')
        start_time = request.POST.get('start_time')
        drop_time = request.POST.get('drop_time')
        if cart_id and travel_date and start_time and drop_time:
            Schedule.objects.create(
                cart_id=cart_id,
                travel_date=travel_date,
                start_time=start_time,
                drop_time=drop_time
            )
            messages.success(request, 'Schedule added successfully.')
            return redirect('admin_schedule_list')
    gocarts = GoCart.objects.all()
    return render(request, 'admin_dashboard/admin_add_schedule.html', {'gocarts': gocarts})

# Edit Schedule
@admin_login_required
def admin_edit_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    if request.method == 'POST':
        schedule.cart_id = request.POST.get('cart')
        schedule.travel_date = request.POST.get('travel_date')
        schedule.start_time = request.POST.get('start_time')
        schedule.drop_time = request.POST.get('drop_time')
        schedule.save()
        messages.success(request, 'Schedule updated successfully.')
        return redirect('admin_schedule_list')
    gocarts = GoCart.objects.all()
    return render(request, 'admin_dashboard/admin_edit_schedule.html', {'schedule': schedule, 'gocarts': gocarts})

# Delete Schedule
@admin_login_required
def admin_delete_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, 'Schedule deleted successfully.')
        return redirect('admin_schedule_list')
    return redirect('admin_schedule_list')

# Bookings
@admin_login_required
def admin_booking_list(request):
    bookings = Booking.objects.select_related('student', 'schedule', 'from_stop', 'to_stop').prefetch_related('seats')
    return render(request, 'admin_dashboard/admin_booking_list.html', {'bookings': bookings})

# Edit Booking
@admin_login_required
def admin_edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    from gocart.models import Stop, Schedule, SeatLayout, User

    if request.method == 'POST':
        booking.student_id = request.POST.get('student')
        booking.schedule_id = request.POST.get('schedule')
        booking.from_stop_id = request.POST.get('from_stop')
        booking.to_stop_id = request.POST.get('to_stop')
        booking.fare = request.POST.get('fare')
        booking.status = request.POST.get('status')
        booking.payment_id = request.POST.get('payment_id')

        selected_seat_ids = request.POST.getlist('seats')
        booking.seats.set(selected_seat_ids)

        booking.save()
        messages.success(request, 'Booking updated successfully.')
        return redirect('admin_booking_list')

    return render(request, 'admin_dashboard/admin_edit_booking.html', {
        'booking': booking,
        'students': User.objects.filter(role='student'),
        'schedules': Schedule.objects.select_related('cart'),
        'stops': Stop.objects.all(),
        'all_seats': SeatLayout.objects.all(),
        'statuses': ['pending', 'confirmed', 'cancelled']
    })

# Delete Booking
@admin_login_required
def admin_delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted successfully.')
    return redirect('admin_booking_list')

# Contact Messages
@admin_login_required
def admin_contact_messages(request):
    messages_qs = ContactMessage.objects.order_by('-timestamp')
    return render(request, 'admin_dashboard/admin_contact_list.html', {'messages': messages_qs})

@admin_login_required
def admin_contact_view(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    return render(request, 'admin_dashboard/admin_contact_view.html', {'message': message})

@admin_login_required
def admin_contact_reply(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    if request.method == 'POST':
        reply_body = request.POST.get('reply_message')
        subject = f"Re: {message.subject}"
        recipient = message.email

        try:
            send_mail(subject, reply_body, settings.DEFAULT_FROM_EMAIL, [recipient])
            message.replied = True
            message.save()
            return render(request, 'admin_dashboard/admin_contact_reply_status.html', {'success': True})
        except BadHeaderError as e:
            return render(request, 'admin_dashboard/admin_contact_reply_status.html', {'success': False, 'error': str(e)})
    return render(request, 'admin_dashboard/admin_contact_reply.html', {'message': message})

@admin_login_required
def admin_contact_delete(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    if request.method == 'POST':
        message.delete()
        messages.success(request, "Message deleted.")
    return redirect('admin_contact_messages')
