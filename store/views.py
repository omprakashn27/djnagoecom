from django.contrib import messages
from store.models import Category, Product
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.

def index(request):
    product = Product.objects.filter(status=0,trending=1,category__status=0)
    category = Category.objects.filter(status=0,trending=1)
    context = {'product':product,'category':category}
    return render(request, 'store/index.html', context)

def collections(request):
    categories = Category.objects.filter(status=0)
    context = {'categories':categories }
    return render(request, 'store/category.html', context)

def collectionsview(request, slug):
    if(Category.objects.filter(slug=slug,status=0)):
        products = Product.objects.filter(category__slug=slug)
        category_name = Category.objects.filter(slug=slug).first
        context = {'products':products, 'category_name': category_name}
        return render(request, 'store/products/index.html', context)
    else:
        messages.error(request, "No Such Category found")
        return redirect('collections')

def productview(request, cate_slug, prod_slug):
    if(Category.objects.filter(slug=cate_slug,status=0)):
        if(Product.objects.filter(slug=prod_slug,status=0)):
            products = Product.objects.filter(slug=prod_slug).first
            context = {'products':products}
        else:
            messages.error(request, "No Such Product found")
            return redirect('collections')
    else:
        messages.error(request, "No Such category found")
        return redirect('collections')
    return render(request, 'store/products/view.html', context)