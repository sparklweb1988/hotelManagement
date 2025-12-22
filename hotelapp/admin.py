from django.contrib import admin

from hotelapp.models import Booking,  Payment, Room, Staff

# Register your models here.

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Staff)
