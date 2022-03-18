from dataclasses import field
from tkinter import Widget
from tkinter.tix import Select
from unicodedata import name
from django.db.models import fields
import django_filters
from django_filters import DateFilter,CharFilter

from .models import * 

class OrderItemFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name="date_created", lookup_expr='gte')
    # end_date = DateFilter(field_name="date_created", lookup_expr='lte')
    
    class Meta:
        model = Order
        fields = ['status']
        
class ProdFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name", lookup_expr='icontains')
    class Meta:
        model = Product
        fields = ['name','company_id','tags']
    
class ProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name", lookup_expr='icontains')
    class Meta:
        model = Product
        fields = ['name']