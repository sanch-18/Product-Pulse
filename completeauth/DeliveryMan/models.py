from django.db import models
from accounts.models import User
# Create your models here.

class DeliveryMan(models.Model):
    email = models.EmailField(default="ABC@gmail.com")
    phone = models.CharField(max_length=12, default="xxxxxxxxxx")
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=15)
    location = models.CharField(max_length=20)
    pincode = models.CharField(max_length=10)
    joined_at = models.DateField()
    is_active = models.BooleanField(default=True)
    salary = models.IntegerField()
    user = models.ForeignKey(User, related_name='Deliver_User', on_delete=models.CASCADE)

    def __str__(self):
        ans = self.name + ' ' + self.city + " " + self.pincode
        return ans