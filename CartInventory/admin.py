from django.contrib import admin
from .models import Item,Category,OrderItem,Order,CartItem
from accounts.models import User
# Register your models here.

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(CartItem)