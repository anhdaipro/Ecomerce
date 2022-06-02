from django.db import models
from order.models import Order
from account.models import User
# Create your models here.
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(null=True)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    def __str__(self):
        return self.user.username
class CancelOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reason = models.TextField(max_length=200,null=True)
    more_information=models.CharField(max_length=300,null=True,blank=True)

