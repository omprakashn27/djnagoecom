from store.models import *
from django.contrib import admin
from store import models
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderItem)
