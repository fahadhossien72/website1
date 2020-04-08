from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class customer(models.Model):
    user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name  = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic= models.ImageField(null=True, blank=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
         return self.name

class Tag(models.Model):
	name  = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name


class product(models.Model):

    CATEGORY = (
    	("indoor","indoor"),
    	("outdoor","outdoor"),
    	)

    name =models.CharField(max_length=100)
    price =models.FloatField(null=True)
    category=models.CharField(max_length=200, choices=CATEGORY)
    date_created= models.DateTimeField(auto_now_add=True, null=True)
    tags=models.ManyToManyField(Tag)

    def __str__(self):
    	return self.name





class order(models.Model):

    STATUS = (
        ("pending","pending"),
        ("On the way","On the way"),
        ("Delivered","Delivered"), 
    	)

    customer = models.ForeignKey(customer, null=True, on_delete=models.SET_NULL)
    product  = models.ForeignKey(product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS)
    note = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.product.name

