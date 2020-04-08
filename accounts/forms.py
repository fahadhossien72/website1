from django .forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import order

class orderForm(ModelForm):
	class Meta:
		model=order
		fields= '__all__'


class CreateUserForm(UserCreationForm):
	class Meta:
		model=User
		fields=['username', 'email', 'password1', 'password2']

def customerForm(ModelForm):
	class Meta:
		model=customer
		fields='__all__'
		exclude=['user']
