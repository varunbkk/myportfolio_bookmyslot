from . import views
from django.urls import path

# We specify an app name to reference the URL we need in our HTML templates
app_name = 'bookmyslot'

# The app(bookmyslot) specific URL's
urlpatterns = [
    path('mybookings/',views.BookingList.as_view(),name='list'),
    path('mybookings/<int:pk>/',views.BookingDetail.as_view(),name='detail'),
    path('update/<int:pk>/',views.BookingUpdate.as_view(),name='update'),
    path('delete/<int:pk>/',views.BookingDelete.as_view(),name='delete'),
    path('new/',views.BookingCreate.as_view(),name='create'),
    path('',views.HomeView.as_view(),name='home'),
    path('welcome/',views.WelcomeView.as_view(),name='welcome'),
    path('thanks/',views.ThanksView.as_view(),name='thanks'),
    path('search/',views.search,name='search_bookings')

]
