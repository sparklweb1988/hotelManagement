from django.db import models

# Create your models here.
class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        ('penthouse', 'Penthouse'),
    ]

    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Room {self.room_number} ({self.get_room_type_display()})"







class Booking(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField( null=True)
    phone_number = models.CharField(max_length=15, null=True)
    address = models.TextField(null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirm', 'Confirmed'), ('cancelled', 'Cancelled')])

    def __str__(self):
        return f"Booking for {self.first_name} {self.last_name}"




class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('CREDIT_CARD', 'Credit Card'), ('CASH', 'Cash'), ('ONLINE', 'Online')])
    status = models.CharField(max_length=20, choices=[('PAID', 'Paid'), ('PENDING', 'Pending'), ('FAILED', 'Failed')])

    def __str__(self):
        return f"Payment for Booking {self.booking.id}"




class Staff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    hire_date = models.DateTimeField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"
