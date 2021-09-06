import json
from django.contrib import messages
from django.http import request
from store.models import Cart, Product
from django.contrib import auth
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# Create your views here.

# @login_required(login_url='login')
def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user.id,product_id=prod_id)):
                    return JsonResponse({'status': 'Product Already in Cart'})
                else:
                    prod_qty = int(request.POST['product_qty'])
                    if product_check.quantity >= prod_qty :
                        cart = Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({'status': "Product Added Successfully"})
                    else:
                        return JsonResponse({'status': 'Only '+ str(product_check.quantity) +' quantity available'})
            else:
                return JsonResponse({'status': "No such product"})
        else:
            return JsonResponse({'status': "Login to continue"})
    return redirect('/')

@login_required(login_url='login')
def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart :
        total_price = total_price + item.product.selling_price * item.product_qty
    context = {'cart':cart,'total_price':total_price}
    return render(request, 'store/cart.html', context)

def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user.id,product_id=prod_id)):
            prod_qty = int(request.POST['product_qty'])
            cart = Cart.objects.get(product_id=prod_id)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status':"Updated successfully"})
    return redirect('/')

def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user.id,product_id=prod_id)):
            cartitem = Cart.objects.get(product_id=prod_id)
            cartitem.delete()
            return JsonResponse({'status':"Item removed from Cart"})
    return redirect('/')
