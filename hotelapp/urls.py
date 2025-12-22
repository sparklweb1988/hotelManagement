from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin_view, name='signin'),
    
    #  ROOM URL
    path('room/', views.room_list,name='room_list'),
    path('room/add/', views.room_add,name='room_add'),
    path('room/update/<int:id>', views.room_update,name='room_update'),
    path('room/delete/<int:id>', views.room_delete,name='room_delete'),
    
 
    
    
    # BOOKING URL
    path('booking/', views.booking_list,name='booking_list'),
    path('booking/add/', views.booking_add,name='booking_add'),
    path('booking/update/<int:id>/', views.booking_update,name='booking_update'),
    path('booking/delete/<int:id>/', views.booking_delete,name='booking_delete'),
    
    
    
    # PAYMENT URL
    path('payment/', views.payment_list,name='payment_list'),
    path('payment/add', views.payment_add,name='payment_add'),
    path('payment/update/<int:id>/', views.payment_update,name='payment_update'),
    path('payment/delete/<int:id>/', views.payment_delete,name='payment_delete'),
    
    
    # STAFF URL
    path('staff/', views.staff_list,name='staff_list'),
    path('staff/add', views.staff_add,name='staff_add'),
    path('staff/update/<int:id>', views.staff_update,name='staff_update'),
    path('staff/delete/<int:id>', views.staff_delete,name='staff_delete'),
   
    
    # LOGOUT
    path('logout/', views.logout_view, name='logout'),
]
