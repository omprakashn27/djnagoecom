import json
from django.contrib import messages
from django.http import request
from store.models import Wishlist, Product
from django.contrib import auth
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# Create your views here.

# @login_required(login_url='login')
def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user.id,product_id=prod_id)):
                    return JsonResponse({'status': 'Product Already in Wishlist'})
                else:
                    wishlist = Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status': "Product Added to Wishlist"})
            else:
                return JsonResponse({'status': "No such product"})
        else:
            return JsonResponse({'status': "Login to continue"})
    return redirect('/')

@login_required(login_url='login')
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist':wishlist}
    return render(request, 'store/wishlist.html', context)

def deletewishlistitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Wishlist.objects.filter(user=request.user.id,product_id=prod_id)):
            wishlistitem = Wishlist.objects.get(product_id=prod_id)
            wishlistitem.delete()
            return JsonResponse({'status':"Item removed from wishlist"})
    return redirect('/')
