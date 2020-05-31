from django.contrib import admin

# Register your models here.
from .models import Topping, Size, Category, Crust, MenuItem, OrderItem, Order

admin.site.register(Topping)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Crust)
admin.site.register(MenuItem)
admin.site.register(OrderItem)
admin.site.register(Order)
