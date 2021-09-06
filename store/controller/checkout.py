import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import request
from django.http import response
from django.http.response import HttpResponse, JsonResponse
from store.models import Cart, Order, OrderItem, Product, Profile
from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import random
# Create your views here.

def view():
    return HttpResponse('hello')

@login_required(login_url='login')
def index(request):
    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart :
        if item.product_qty > item.product.quantity :
            Cart.objects.delete(id=item.id)

    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems :
        total_price = total_price + item.product.selling_price * item.product_qty

    userprofile = Profile.objects.filter(user=request.user).first()

    context = {'cartitems':cartitems , 'total_price':total_price, 'userprofile':userprofile}
    return render(request, 'store/checkout.html', context)

@login_required(login_url='login')
def placeorder(request):
    if request.method == 'POST':

        currentuser = User.objects.filter(id=request.user.id).first()

        if not currentuser.first_name :
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()

        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address1 = request.POST.get('address1')
            userprofile.address2 = request.POST.get('address2')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address1 = request.POST.get('address1')
        neworder.address2 = request.POST.get('address2')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart :
            cart_total_price = cart_total_price + item.product.selling_price * item.product_qty

        neworder.total_price = cart_total_price
        neworder.message = request.POST.get('message')
        
        trackno = 'sharma'+str(random.randint(11111111,99999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'sharma'+str(random.randint(11111111,99999999))

        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(order=neworder, product=item.product, price=item.product.selling_price,quantity=item.product_qty)

            # To decrease the product quantity
            orderproduct = Product.objects.filter(id=item.product.id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_qty
            orderproduct.save()

        # To clear the user's cart
        Cart.objects.filter(user=request.user).delete()

        messages.success(request, "Your order has been placed successfully")
        p_mode = request.POST.get('payment_mode')
        if(p_mode == 'PayPal' or p_mode == 'Paid by Razorpay'):
            return JsonResponse({'status':"Your order has been placed successfully"})
    return redirect('/')

@login_required(login_url='login')
def razorpaycheck(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        payment_mode = request.POST.get('payment_mode')
        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart :
            cart_total_price = cart_total_price + item.product.selling_price * item.product_qty

        return JsonResponse({
            'fname':fname,
            'lname':lname,
            'email':email,
            'phone':phone,
            'address1':address1,
            'address2':address2,
            'city':city,
            'state':state,
            'country':country,
            'pincode':pincode,
            'payment_mode':payment_mode,
            'cart_total_price':cart_total_price,
        })
