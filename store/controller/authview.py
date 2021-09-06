from store.models import Order, OrderItem
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from store.forms import CustomUserForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages


def loginPage(request):
    if request.user.is_authenticated :
        messages.success(request,'You are already logged in')
        return redirect("/")
    else :
        if request.method == "POST":
            name = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=name, password=password)

            if user is not None:
                login(request, user)
                messages.success(request,'Logged in successfully')
                return redirect("/")
            else:
                messages.success(request,'Invalid Username or password')
                return redirect("/login")
                return 0

    return render(request, "store/auth/login.html")

def logoutPage(request):
    logout(request)
    messages.success(request,'Logged out successfully')
    return redirect('/')

def registerPage(request):
    form = CustomUserForm()

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registered successfully !! Login to continue')
            return redirect("/login")

    context = {'form':form}
    return render(request, "store/auth/register.html",context)

def orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders':orders}
    return render(request, 'store/orders/index.html', context)

def orderview(request, t_no):
    order = Order.objects.filter(user=request.user).filter(tracking_no=t_no).first()
    orderitems = OrderItem.objects.filter(order=order)
    context = {'orderitems':orderitems, 'order':order}
    return render(request, 'store/orders/view.html', context)
    