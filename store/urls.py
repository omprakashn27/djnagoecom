from store.models import Wishlist
from django.contrib import admin
from django.urls import path
from store import views
from store.controller import cart, authview, checkout, wishlist


admin.site.site_header = "Sharma Coder"
admin.site.site_title = "Sharma Coder Login Admin Dashboard"
admin.site.index_title = "Sharma Coder Admin Dashboard"

urlpatterns = [
    path('', views.index, name="/"),
    path('collections', views.collections, name="collections"),
    path('collections/<str:slug>', views.collectionsview, name="collectionsview"),
    path('collections/<str:cate_slug>/<str:prod_slug>', views.productview, name="productview"),

    path('login/', authview.loginPage, name="login"),
    path('register/', authview.registerPage, name="register"),
    path('logout/', authview.logoutPage, name="logout"),

    path('cart', cart.viewcart, name="cart"),
    path('add-to-cart', cart.addtocart, name="addtocart"),
    path('update-cart', cart.updatecart, name="updatecart"),
    path('delete-cart-item', cart.deletecartitem, name="deletecartitem"),

    path('wishlist', wishlist.index , name="wishlist"),
    path('add-to-wishlist', wishlist.addtowishlist, name="addtowishlist"),
    path('delete-wishlist-item', wishlist.deletewishlistitem, name="deletewishlistitem"),

    path('checkout', checkout.index, name='checkout'),
    path('place-order', checkout.placeorder, name='placeorder'),

    path('orders', authview.orders, name='orders'),
    path('view-order/<str:t_no>', authview.orderview, name="orderview"),

    path('proceed-to-pay', checkout.razorpaycheck),
    
]
