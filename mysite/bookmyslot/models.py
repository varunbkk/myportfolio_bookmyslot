from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

class Customer(models.Model):
    # username is defined as FK to Django's User model, because a single user can have multiple customers
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.name

# Create your models here.
class Booking(models.Model):
    # Similarly, customer_name is defined as FK to the Customer model, because a single customer can have multiple bookings
    customer_name = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    qty_plts = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(50)])
    cbm = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(50)])
    created_date = models.DateTimeField(default=timezone.now())
    delivery_details = models.DateTimeField(null=True)
    booking_number = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.booking_number

    # We use the save() function to concatenate the delivery date and time components of the delivery_details field
    # into the booking_number field
    def save(self, **kwargs):

        self.booking_number = f"{self.delivery_details:%Y%m%d%H%M}"
        super().save(**kwargs)

    # this provides the url for viewing an instance of the model object, once it is creatd.
    # Instance of an object means a specific booking, which is denoted by a unique primary key(pk)
    def get_absolute_url(self):
        return reverse('bookmyslot:detail',kwargs={'pk':self.pk})
