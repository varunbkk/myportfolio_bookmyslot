from django.shortcuts import render

# Create your views here.
from .models import Booking,Customer
from .forms import BookingForm
from django.urls import reverse,reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,DetailView,CreateView,UpdateView,DeleteView,TemplateView)
from django.db.models import Q

import datetime as dt
from django.utils import timezone

class AboutView(TemplateView):
    template_name = 'about.html'

class HomeView(TemplateView):
    template_name = 'index.html'

class BookingCreate(LoginRequiredMixin,CreateView):
    login_url = '/login'
    redirect_field_name = 'bookmyslot/booking_detail.html'
    model = Booking
    form_class = BookingForm

    # This function returns a dictionary that is passed to the __init__ portion of our Booking form
    # We need to pass the current username to the form so that only the customers belonging to that specific username
    # can be visible in the drop-down list

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(BookingCreate,self).get_form_kwargs(**kwargs)
        form_kwargs['username'] = self.request.user
        return form_kwargs

    # This function validates the form before the form data is written to the database/model
    # The form data is only stored in the memory (with the commit=False statement)
    # It also insures that the user creating the form is the same as the currently logged in user
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = self.request.user
        self.object.save()
        return super().form_valid(form)

class BookingList(LoginRequiredMixin,ListView):
    login_url = '/login'
    model = Booking
    # We paginate the list of bookings and limit 3 booking per each page
    paginate_by = 3
    template_name = 'bookmyslot/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Booking.objects.filter(username=self.request.user).exclude(delivery_details__date__lte=dt.date.today()).order_by('delivery_details')
        else:
            return Booking.objects.all()

class BookingDetail(LoginRequiredMixin,DetailView):
    login_url = '/login'
    context_object_name = 'booking_detail'

    model = Booking
    def get_queryset(self):
        if not self.request.user.is_staff:
            return Booking.objects.filter(username=self.request.user)
        else:
            return Booking.objects.all()

class BookingUpdate(LoginRequiredMixin,UpdateView):
        login_url = '/login'
        template_name = 'bookmyslot/booking_form_update.html'
        model = Booking
        form_class = BookingForm

        # Identical to what we did in the CreateView class
        def get_form_kwargs(self, **kwargs):
            form_kwargs = super(BookingUpdate,self).get_form_kwargs(**kwargs)
            form_kwargs['username'] = self.request.user
            return form_kwargs

        def form_valid(self, form):
            self.object = form.save(commit=False)
            self.object.username = self.request.user
            self.object.save()
            return super().form_valid(form)

class BookingDelete(LoginRequiredMixin,DeleteView):
    login_url = '/login'
    model = Booking
    success_url = reverse_lazy('bookmyslot:list')

# We're using a function-based view to get search results for bookings, based on the keywords that a user enters
# The user can search by delivery date or the booking number
@login_required
def search(request):
    query = request.GET.get('q')

    if query:
        object_list = Booking.objects.filter(username=request.user).filter(Q(booking_number__icontains=query) | Q(delivery_details__date__icontains=query)).exclude(delivery_details__date__lte=dt.date.today()).order_by('delivery_details')

        result = object_list
    else:
        result = []

    return render(request,'bookmyslot/search_bookings.html',{'result':result,'query':query})
