from http.client import HTTPResponse
from django.db import IntegrityError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required

from hotelapp.models import  Booking, Payment, Room, Staff



def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            try:
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('room_list')
            except IntegrityError:
                return render(request, 'accounts/signin.html', {'error': 'Username already taken. Please choose another one.'})
        else:
            return render(request, 'accounts/signin.html', {'error': 'Username and password are required.'})

    return render(request, 'accounts/signin.html')





#  ROOM VIEWS
@login_required
def room_list(request):
    rooms = Room.objects.all()
    context = {
        'rooms':rooms
    }
    return render(request, 'main/room_list.html',context)

# ADD ROOM
@login_required
def room_add(request):
    if request.method =='POST':
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('room_type')
        price_per_night = request.POST.get('price_per_night')
        is_available = request.POST.get('is_available') =='True'
        description = request.POST.get('description')
        
        
        new_room = Room(room_number=room_number,room_type=room_type,price_per_night=price_per_night,is_available=is_available,
                        description=description)
        
        new_room.save()
        return redirect('room_list')
    return render(request, 'main/room_add.html')


# UPDATE ROOM VIEW
@login_required
def room_update(request,id):
    rooms = get_object_or_404(Room, pk=id)
    if request.method =='POST':
        rooms.room_number = request.POST.get('room_number')
        rooms.room_type = request.POST.get('room_type')
        rooms.price_per_night = request.POST.get('price_per_night')
        rooms.is_available = request.POST.get('is_available') =='True'
        rooms.description = request.POST.get('description')
        
        rooms.save()
        return redirect('room_list')
    return render(request, 'main/update_room.html',{'rooms':rooms})


#  DELETE VIEW
@login_required
def room_delete(request,id):
    rooms = get_object_or_404(Room,pk=id)
    rooms.delete()
    return redirect('room_list')

# BOOKING VIEWS
@login_required
def booking_list(request):
    bookings = Booking.objects.all()
    
    context = {
        'bookings':bookings
    }
    return render(request, 'main/booking_list.html',context)

# ADD BOOKING VIEW
@login_required
def booking_add(request):
    rooms = Room.objects.filter(is_available=True)  # Get only available rooms
    if request.method == 'POST':
      
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        room_id = request.POST.get('room')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        total_price = request.POST.get('total_price')
        status = request.POST.get('status')

        
        if not all([first_name, last_name, email, phone_number, address, room_id, check_in, check_out, total_price, status]):
            return HttpResponseBadRequest("All fields are required.")

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
           
            return HttpResponseBadRequest("The selected room does not exist.")
        
        
        new_booking = Booking(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address=address,
            room=room,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
            status=status
        )
        new_booking.save()
        
        return redirect('booking_list')  

    return render(request, 'main/booking_add.html', {'rooms': rooms})


# UPDATE BOOKING VIEW
@login_required
def booking_update(request, id):
    booking = get_object_or_404(Booking, id=id)   # ✅ SINGLE booking
    rooms = Room.objects.filter(is_available=True)  # ✅ for dropdown

    if request.method == 'POST':
        booking.first_name = request.POST.get('first_name')
        booking.last_name = request.POST.get('last_name')
        booking.email = request.POST.get('email')
        booking.phone_number = request.POST.get('phone_number')
        booking.address = request.POST.get('address')
        booking.room_id = request.POST.get('room')
        booking.check_in = request.POST.get('check_in')
        booking.check_out = request.POST.get('check_out')
        booking.total_price = request.POST.get('total_price')
        booking.status = request.POST.get('status')
        booking.save()

        return redirect('booking_list')

    return render(request, 'main/booking_update.html', {
        'booking': booking,
        'rooms': rooms
    })




#  DELETE BOOKING VIEW
@login_required
def booking_delete(request, id):
    bookings= get_object_or_404(Booking,pk=id)
    bookings.delete()
    return redirect('booking_list')

#  ADD PAYMENT VIEW

@login_required
def payment_list(request):
    payments = Payment.objects.all()
    context = {'payments':payments}
    return render(request, 'main/payment_list.html', context)



@login_required
def payment_add(request):
    bookings = Booking.objects.all()

    if request.method == 'POST':
        booking_id = request.POST.get('booking')

        if not booking_id:
            return HttpResponseBadRequest("Booking is required.")

        booking = get_object_or_404(Booking, id=booking_id)

        payment = Payment.objects.create(
            booking=booking,
            payment_date=request.POST.get('payment_date'),
            amount_paid=request.POST.get('amount_paid'),
            payment_method=request.POST.get('payment_method'),
            status=request.POST.get('status'),
        )

        return redirect('payment_list')

    return render(request, 'main/payment_add.html', {'bookings': bookings})



#  DELETE BOOKING VIEW
@login_required
def booking_delete(request, id):
    bookings= get_object_or_404(Booking,pk=id)
    bookings.delete()
    return redirect('booking_list')

#  ADD PAYMENT VIEW

@login_required
def payment_list(request):
    payments = Payment.objects.all()
    context = {'payments':payments}
    return render(request, 'main/payment_list.html', context)



@login_required
def payment_add(request):
    bookings = Booking.objects.all()

    if request.method == 'POST':
        booking_id = request.POST.get('booking')

        if not booking_id:
            return HttpResponseBadRequest("Booking is required.")

        booking = get_object_or_404(Booking, id=booking_id)

        payment = Payment.objects.create(
            booking=booking,
            payment_date=request.POST.get('payment_date'),
            amount_paid=request.POST.get('amount_paid'),
            payment_method=request.POST.get('payment_method'),
            status=request.POST.get('status'),
        )

        return redirect('payment_list')

    return render(request, 'main/payment_add.html', {'bookings': bookings})


#  UPDATE PAYMENT VIEW


@login_required
def payment_update(request, id):
    
    payment = get_object_or_404(Payment, id=id)
    bookings = Booking.objects.all()  

    if request.method == 'POST':
        booking_id = request.POST.get('booking')

        if not booking_id:
            return HttpResponseBadRequest("Booking is required.")

  
        booking = get_object_or_404(Booking, id=booking_id)

      
        payment.booking = booking
        payment.payment_date = request.POST.get('payment_date')
        payment.amount_paid = request.POST.get('amount_paid')
        payment.payment_method = request.POST.get('payment_method')
        payment.status = request.POST.get('status')
  
        payment.save()

        return redirect('payment_list')

    return render(request, 'main/update_payment.html', {
        'payment': payment,
        'bookings': bookings
    })


#  DELETE VIEW
@login_required
def payment_delete(request,id):
    payments = get_object_or_404(Payment, pk=id)
    payments.delete()
    return redirect('payment_list')


# STAFF VIEWS
@login_required
def staff_list(request):
    staffs = Staff.objects.all()
    return render(request, 'main/staff_list.html',{'staffs':staffs})

# ADD STAFF VIEW
@login_required

def staff_add(request):
    if request.method =='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        hire_date = request.POST.get('hire_date')
        
        
        staff = Staff.objects.create(first_name=first_name,last_name=last_name,role=role,email=email,phone_number=phone_number,
                                     hire_date=hire_date)
        staff.save()
        return redirect('staff_list')
    return render(request, 'main/staff_add.html')



#  UPDATE STAFF VI
@login_required
def staff_update(request, id):
   
    staff = get_object_or_404(Staff, id=id)

    if request.method == 'POST':
     
        staff.first_name = request.POST.get('first_name')
        staff.last_name = request.POST.get('last_name')
        staff.role = request.POST.get('role')
        staff.email = request.POST.get('email')
        staff.phone_number = request.POST.get('phone_number')
        staff.hire_date = request.POST.get('hire_date')

        # Save the updated staff data
        staff.save()

        # Redirect to the staff list page after the update
        return redirect('staff_list')

    # If GET request, render the form with the current staff data
    return render(request, 'main/staff_update.html', {
        'staff': staff
    })



#  STAFF DELETE VIEW
@login_required
def  staff_delete(request, id):
    staffs = get_object_or_404(Staff, pk=id)
    staffs.delete()
    return redirect('staff_list')



# LOGOUT VIEWA

def logout_view(request):
    logout(request)
    return redirect('signin')
