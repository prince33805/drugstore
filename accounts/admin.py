from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Company)
admin.site.register(Medicine)
admin.site.register(Employee)