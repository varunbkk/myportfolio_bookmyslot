from django import forms
from django.forms import Form, ChoiceField, CharField, HiddenInput
from bookmyslot.models import Booking,Customer
from bootstrap_datepicker_plus import DatePickerInput,DateTimePickerInput
import datetime as dt
from django.utils import timezone
from .utilities import check_free_time
import os
from datetime import date


class BookingForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        # This pops the username from kwargs that was passed as a dictionary from get_form_kwargs() in the CreateView/UpdateView classes
        user = kwargs.pop('username',None)
        super(BookingForm,self).__init__(*args,**kwargs)
        self.fields['qty_plts'].label = "Quantity Of Pallets"
        self.fields['cbm'].label = "Shipment CBM"
        self.fields['delivery_details'].label = "Delivery Date/Time"
        self.fields['customer_name'].label = "Customer Name"
        # Finally, we run a queryset to filter the customer_name limited to the specific username from the Customer model
        self.fields['customer_name'].queryset = Customer.objects.filter(username=user)

    def clean(self):
        cleaned_data = super(BookingForm,self).clean()
        cleaned_delivery_details = cleaned_data.get('delivery_details')
        cleaned_booking_number = f"{cleaned_delivery_details:%Y%m%d%H%M}"

        if Booking.objects.filter(booking_number=cleaned_booking_number).exists():
            d = cleaned_delivery_details.day
            m = cleaned_delivery_details.month
            y = cleaned_delivery_details.year

            # Retrieve today's bookings
            today_bookings = Booking.objects.filter(delivery_details__year=y,delivery_details__month=m,delivery_details__day=d)

            # A list of today's bookings time slot (take only hours)
            # Return something like <QuerySet [{'delivery_date__hour': 11}, ...]>
            today_time_slot = today_bookings.values('delivery_details__hour')
            # Convert it to list of hours values since the utility function accept list.
            today_time_slot_list = [h['delivery_details__hour'] for h in list(today_time_slot)]
            # The line above return something like [9, 11, ...]

            all_time_slot = [7, 8, 9, 10, 11, 12]

            # Now we can call the utility function `check_free_time`
            available_slot = check_free_time(all_time_slot, today_time_slot_list)

            if available_slot:
                message = f"Requested slot is already booked, please choose another time in {available_slot}."
                raise forms.ValidationError(message)
            else:  # The list is empty, all slot are taken
                message = "The are not available slot for this booking today."
                raise forms.ValidationError(message)

    # The Meta class provides metadata to the Modelform class
    # This basically tells the form which model to use, the list of fields to include in the form
    # and to specify any relevant widgets - herein we are using a third-party bootstrap datepicker widget - >DatePickerInput()
    class Meta:
        model = Booking
        min_date = timezone.now() + dt.timedelta(days=1)
        max_date = timezone.now() + dt.timedelta(days=30)
        delivery_details = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])
        fields = ('customer_name','qty_plts','cbm','delivery_details')
        widgets = {'delivery_details':DateTimePickerInput(
                        options={
                                "daysOfWeekDisabled":[0,6],
                                "minDate":min_date.strftime('%Y-%m-%d'),
                                "maxDate":max_date.strftime('%Y-%m-%d'),
                                "format": "YYYY-MM-DD hh:00",
                                "enabledHours": [7,8,9,10,11,12],
                                "showClear": False,

                                }
                                                        )
                    }
