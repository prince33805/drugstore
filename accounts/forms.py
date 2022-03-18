from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Customer, Employee, Order , Company , Medicine , Product
from accounts import models

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']
        
class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__' 
        # labels = {
        #     'name':'',
        #     'address':'',
        #     'phone':'',
        #     'email':'',
        #     'description':'',   
        # }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone','pattern':'[0-9]{10}'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),       
        }

class ProductForm(ModelForm):
    class Meta:
        model = Product 
        fields = ['company_id','name','medical_typ','description','buy_price','price','qty','tags']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'name'}),
            'buy_price':forms.NumberInput(attrs={'class':'form-control','placeholder':'buy_price'}),
            'qty':forms.NumberInput(attrs={'class':'form-control','placeholder':'qty'}),
            'company_id':forms.Select(attrs={'class':'form-control','placeholder':'company_id'}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':'description'}),
            'medical_typ':forms.TextInput(attrs={'class':'form-control','placeholder':'medical Type'}),
            'price':forms.NumberInput(attrs={'class':'form-control','placeholder':'price'}),
            'tags':forms.SelectMultiple(attrs={'class':'form-control','placeholder':'tags'}),
        }
        
class EmployeeForm(ModelForm):
    class Meta:
        model = Employee 
        fields = ['name','phone','email','joining_date']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'phone','pattern':'[0-9]{10}'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            'joining_date':forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','phone','email','address','district','amphoe','province','zipcode']
        exclude = ['user']
        labels = {
            'name':'ชื่อ',
            'email':'อีเมลล์',
            'address':'ที่อยู่',
            'district':'ตำบล',
            'amphoe':'อำเภอ',
            'province':'จังหวัด',
            'zipcode':'รหัสไปรษณีย์',
            'phone':'เบอร์ไทร',
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'address'}),
            'district':forms.TextInput(attrs={'class':'form-control','placeholder':'district'}),
            'amphoe':forms.TextInput(attrs={'class':'form-control','placeholder':'amphoe'}),
            'province':forms.TextInput(attrs={'class':'form-control','placeholder':'province'}),
            'zipcode':forms.TextInput(attrs={'class':'form-control','placeholder':'zipcode'}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'phone','pattern':'[0-9]{10}'}),
            # 'joining_date':forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }
