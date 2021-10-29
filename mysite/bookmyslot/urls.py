from . import views
from django.urls import path

app_name = 'bookmyslot'

urlpatterns = [
    path('mybookings/',views.BookingList.as_view(),name='list'),
    path('mybookings/<int:pk>/',views.BookingDetail.as_view(),name='detail'),
    path('update/<int:pk>/',views.BookingUpdate.as_view(),name='update'),
    path('delete/<int:pk>/',views.BookingDelete.as_view(),name='delete'),
    path('new/',views.BookingCreate.as_view(),name='create'),
    path('',views.HomeView.as_view(),name='home'),
    path('about/',views.AboutView.as_view(),name='about'),
    path('search/',views.search,name='search_bookings')

]
