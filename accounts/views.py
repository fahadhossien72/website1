from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from . models import*
from .forms import orderForm,CreateUserForm,customerForm
from .filters import orderFilter
from django.contrib import messages
from . decorators import unauthenticated_user, allowed_users,admin_only


# Create your views here.
#@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def home(request):
	orders = order.objects.all()
	customers = customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending=orders.filter(status='pending').count

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products= product.objects.all()
	return render(request, "accounts/product.html",{'products':products})


#@login_required(login_url='login')
#@allowed_users(allowed_roles='admin')
def custom(request, pk_test):
	custom=customer.objects.get(id=pk_test)
	orders = custom.order_set.all()
	order_count=orders.count()
	myFilter=orderFilter(request.GET, queryset=orders)
	orders=myFilter.qs
	context={'custom':custom,'orders':orders,'order_count':order_count,'myFilter':myFilter}
	return render(request, "accounts/customer.html",context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
	custom=customer.objects.get(id=pk)
	orderFormSet=inlineformset_factory(customer,order, fields=('product','status'), extra=5)
	formset=orderFormSet(queryset=order.objects.none(), instance=custom)
	#form=orderForm(initial={'customers':custom})
	#form=orderForm()
	if request.method=='POST':
		formset=orderFormSet(request.POST, instance=custom)
		if formset.is_valid():
			formset.save()
			return redirect('/')
	context={'formset':formset}
	return render(request, "accounts/order_form.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
	orders=order.objects.get(id=pk)
	form=orderForm(instance=orders)
	if request.method=="POST":
		form=orderForm(request.POST, instance=orders)
		if form.is_valid():
			form.save()
			return redirect('/')
	context={'form':form}
	return render(request,"accounts/order_form.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
	orders=order.objects.get(id=pk)
	form=orderForm()
	if request.method=="POST":
		orders.delete()
		return redirect('/')
	context={'orders':orders}
	return render(request, "accounts/delete.html",context)



def loginform(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@unauthenticated_user   
def registerform(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user=form.save()
			group= Group.objects.get(name='customer')
			user.groups.add(group)
			customer.objects.create(user=user)
			username = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + username)

			return redirect('login')

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@allowed_users(allowed_roles=['customer']) 
def loginpage(request):
	orders= request.user.customer.order_set.all()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending=orders.filter(status='pending').count
	context={'orders':orders, 'total_orders': total_orders, 'delivered':delivered, 'pending':pending}
	return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer']) 
def accountSettings(request):
	customer = request.user.customer
	form = customerForm(instance=customer)

	if request.method == 'POST':
		form = customerForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)