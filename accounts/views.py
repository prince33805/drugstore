from itertools import count
from re import T
from django.db.models import query,Max,Min,Sum,Count
from django.shortcuts import render,redirect
from django.http import HttpResponse , JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import json
from datetime import datetime , timedelta, time

from accounts import admin

# Create your views here.
from .models import *
from .forms import CompanyForm, ProductForm, OrderForm , CreateUserForm , CustomerForm,EmployeeForm , UserUpdateForm 
from .filters import OrderItemFilter , ProdFilter , ProductFilter
from .decorators import unauthenticated_user , allowed_users , admin_only
from .utils import *
from django.db.models import Q

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def store(request):
    data  = cartData(request)
    cartItems = data['cartItems']
    profile = []
    products = Product.objects.all()
    tags = Tag.objects.all()
    
        
    if request.user.is_authenticated:
        profile = Customer.objects.get(user=request.user)
        
    search = False
    search_post = request.GET.get('search')
    empty = False
    # print(search_post)
    
    if search_post:
        products = Product.objects.filter(Q(name__icontains=search_post) | Q(description__icontains=search_post))
        search = True
        print (products)
        if products.count() == 0:
            products = Product.objects.all()
            empty = True
        else:
            products = Product.objects.filter(Q(name__icontains=search_post) | Q(description__icontains=search_post))
        # myFilter = ProductFilter(request.GET, queryset=products)
        # products = myFilter.qs
    else:
        # If not searched, return default posts
        products = Product.objects.all()
    
    context={'products':products,'cartItems':cartItems,'profile':profile,
             'tags':tags,'search':search,'search_post':search_post,'empty':empty}
    return render(request,'store/store.html',context)

def category(request,pk_test):
    
    data  = cartData(request)
    cartItems = data['cartItems']
    profile = []
    tags = Tag.objects.all()
    # print(tags)
    tag = Tag.objects.get(id=pk_test)
    
    if request.user.is_authenticated:
        profile = Customer.objects.get(user=request.user)
    
    products = Product.objects.filter(tags=pk_test)
    
    context={'products':products,'cartItems':cartItems,'profile':profile,'tags':tags,'tag':tag}
    return render(request,'store/category.html',context)

def viewProduct(request,pk_test):
    
    product = Product.objects.get(id=pk_test)
    profile = []
    if request.user.is_authenticated:
        profile = Customer.objects.get(user=request.user)
    
    tags = Tag.objects.all()
    
    data  = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'product':product,'items':items,'order':order,'cartItems':cartItems,'profile':profile,'tags':tags}
    return render(request,'store/view_product.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def cart(request):
    profile = Customer.objects.get(user=request.user)
    tags = Tag.objects.all()
    
    data  = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context={'items':items,'order':order , 'cartItems':cartItems,'profile':profile,'tags':tags}
    return render(request,'store/cart.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def checkout(request):
    profile = Customer.objects.get(user=request.user)
    tags = Tag.objects.all()
    
    data  = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    print(data)
    
    context={'items':items,'order':order,'cartItems':cartItems,'profile':profile,'tags':tags}
    
    if cartItems == 0:
        return redirect('store')
    else:
        return render(request,'store/checkout.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action:', action)
    print('productId:', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order , created = Order.objects.get_or_create(customer=customer,complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        orderItem.item_total_price = orderItem.get_total
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        orderItem.item_total_price = orderItem.get_total
    
    orderItem.save()

    get_total = orderItem.get_total
    print(get_total)
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added' , safe = False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def processOrder(request):
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,complete=False)
        
    total = float(data['form']['total'])
    # itemtotal = float(data['form']['itemtotal'])
    if total == float(order.get_cart_total):
        order.complete = True
        order.order_total_price = total
        order.order_total_quantity = order.get_cart_items
        order.date_created = datetime.now()
    order.save()
    
    return JsonResponse('Ordering successful!',safe=False)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def profile(request):
    profile = Customer.objects.get(user=request.user)
    # print(profile.id)
    showorder = Order.objects.filter(customer=profile.id).order_by('-date_created')[1:]
    # print(showorder)
    tags = Tag.objects.all()       
       
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']
    
    context = {'profile':profile,'items':items,'cartItems':cartItems,
               'showorder':showorder,'tags':tags}
    return render(request,'store/profile.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def profileUpdate(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']
    
    profile = Customer.objects.get(user=request.user)
    # print(profile)
    tags = Tag.objects.all()
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=profile)
        if u_form.is_valid():
            u_form.save()
            return redirect('/profile')
    else:
        u_form = UserUpdateForm(instance=profile)
        
    context = {
        'u_form': u_form,
        'items':items,'cartItems':cartItems,'profile':profile,'tags':tags
    }
    return render(request, 'store/profile_update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def cusViewOrder(request,pk_test):
    profile = Customer.objects.get(user=request.user)
    
    order = Order.objects.get(id=pk_test)
    orderitem = OrderItem.objects.filter(order=order.id)
    tags = Tag.objects.all()
    
    data  = cartData(request)
    cartItems = data['cartItems']
    context = {'order':order,'orderitem':orderitem,'cartItems':cartItems,'tags':tags,'profile':profile}
    return render(request,'store/view_order.html',context)

@unauthenticated_user
def registerPage(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            messages.success(request,'Account was created for ' + username)
            return redirect('login')
        
    context = {'form':form}
    return render(request , 'accounts/register.html',context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request , username=username , password=password) 
        if user is not None:            
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username OR Password is incorrect')
            
    context = {}
    return render(request , 'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

##########################################################

##########################################################

##########################################################

##########################################################


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def home(request):
    
    orders = Order.objects.all()
    total_orders = orders.count()
    customers = Customer.objects.all()
    total_customers = customers.count()
    products = Product.objects.all()
    total_products = products.count()
    orderitems = OrderItem.objects.all()
    medicines = Product.objects.filter(qty__lte=200)
    
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    date_from = datetime.now() - timedelta(days=6)
    countorderweek = Order.objects.filter(date_created__gte=date_from).count()
    
    oi = orderitems.filter(date_added__gte=date_from).values('product','product__name','product__price').annotate(n=Sum('quantity')).order_by('-n')[:5]
    oiworst = orderitems.filter(date_added__gte=date_from).values('product','product__name','product__price').annotate(n=Sum('quantity')).order_by('n')[:5]
    # oi = OrderItem.objects.aggregate(Sum('quantity')) .values('product')  
    # print(oi)
    
    context = {'orders': orders,'customers': customers , 'medicines':medicines,'countorderweek':countorderweek, 
               'total_customers':total_customers,'total_orders':total_orders,'total_products':total_products,
               'delivered':delivered,'pending':pending,'oi':oi,'oiworst':oiworst
               }
    
    return render(request,'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()

	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def company(request):
    form = CompanyForm()
    allcompany = Company.objects.all()
    
    print(allcompany) 
    submitted = False
    if request.method == 'POST':
        # print(request.POST)
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/company?submitted=True')
    else:
        form = CompanyForm
        if 'submitted' in request.GET:
            submitted = True
        
    context = {'form':form,'submitted':submitted,'allcompany':allcompany}
    return render(request,'accounts/company.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def viewCompany(request,pk_test):
    
    company = Company.objects.get(id=pk_test)
    form = CompanyForm(instance=company)
    medicines = Product.objects.filter(company_id=pk_test)
    # print(medicine) 
    
    context = {'company':company,'form':form,'medicines':medicines}
    return render(request,'accounts/view_company.html',context)

@login_required(login_url='login')
@admin_only
def updateCompany(request,id):
    
    company = Company.objects.get(pk=id)
    form = CompanyForm(request.POST or None , instance=company)
    # print(company)
    if form.is_valid():
        form.save()
        # print(company)
        return redirect('/company')

    context = {'company':company,'form':form}
    return render(request,'accounts/update_company.html',context)

@login_required(login_url='login')
@admin_only
def deleteCompany(request,id):
    
    company = Company.objects.get(pk=id)
    if request.method == "POST":
        company.delete()
        return redirect('/company')
        
    context = {'company':company}
    return render(request,'accounts/delete_company.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def medicine(request):
    form = ProductForm()
    allmedicine = Product.objects.all()
    medfilter = ProdFilter(request.GET,queryset=allmedicine)
    allmedicine = medfilter.qs
    
    # print(medfilter) 
    submitted = False
    if request.method == 'POST':
        # print(request.POST)
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/medicine?submitted=True')
    else:
        form = ProductForm
        if 'submitted' in request.GET:
            submitted = True
        
    context = {'form':form,'submitted':submitted,'allmedicine':allmedicine,'medfilter':medfilter}
    return render(request,'accounts/medicine.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def viewMedicine(request,pk_test):
    
    medicine = Product.objects.get(id=pk_test)
    form = ProductForm(instance=medicine)
    medtags = list(Product.tags.through.objects.filter(product__id=pk_test).values_list('tag__name', flat=True))
    # tags = Tag.objects.filter(id=medtags)
    print(medtags)
    
    context = {'medicine':medicine,'form':form,'medtags':medtags}
    return render(request,'accounts/view_medicine.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def updateMedicine(request,id):
    
    medicine = Product.objects.get(pk=id)
    form = ProductForm(request.POST or None , instance=medicine)
    # print(company)
    if form.is_valid():
        form.save()
        print(company)
        return redirect('/medicine')

    context = {'medicine':medicine,'form':form}
    return render(request,'accounts/update_medicine.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def employee(request):
    form = EmployeeForm()
    allemployee = Employee.objects.all()
    
    # print(allemployee) 
    submitted = False
    if request.method == 'POST':
        # print(request.POST)
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/employee?submitted=True')
    else:
        form = EmployeeForm
        if 'submitted' in request.GET:
            submitted = True 
            
    context = {'form':form,'submitted':submitted,'allemployee':allemployee}
    return render(request,'accounts/employee.html',context)

@login_required(login_url='login')
@admin_only
def updateEmployee(request,id):
    
    employee = Employee.objects.get(id=id)
    form = EmployeeForm(request.POST or None , instance=employee)
    # print(company)
    if form.is_valid():
        form.save()
        # print(company)
        return redirect('/employee')

    context = {'employee':employee,'form':form}
    return render(request,'accounts/update_employee.html',context)

@login_required(login_url='login')
@admin_only
def deleteEmployee(request,id):
    
    employee = Employee.objects.get(id=id)
    if request.method == "POST":
        employee.delete()
        return redirect('/employee')
        
    context = {'employee':employee}
    return render(request,'accounts/delete_employee.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def customer(request):
    customer = Customer.objects.all
    
    context = {'customer':customer}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def customerDetail(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    
    orders = customer.order_set.all()
    order_count = orders.count()
    
    qset = Order.objects.filter(customer=customer).order_by('-date_created')
    # qsetcount = qset.count()
    
    myFilter = OrderItemFilter(request.GET, queryset=qset)
    qset = myFilter.qs
    
    context = {'customer':customer,'orders':orders,'order_count':order_count,
               'myFilter':myFilter,'qset':qset}
    return render(request,'accounts/customer_detail.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def order(request):
    
    order = Order.objects.all().order_by('-date_created')
    myFilter = OrderItemFilter(request.GET,queryset=order)
    order = myFilter.qs
    
    context = {'order':order,'myFilter':myFilter}
    return render(request,'accounts/order.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def viewOrder(request,pk_test):
    order = Order.objects.get(id=pk_test)
    orderitem = OrderItem.objects.filter(order=order.id)
    print(orderitem)
    
    form = OrderForm()
    if request.method == 'POST':
        # print('Printing POST:',request.POST)
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('order')
    
    context = {'order':order,'orderitem':orderitem,'form':form}
    return render(request,'accounts/view_order.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order , fields=('product','status'), extra=10 )
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing POST:',request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    
    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','employee'])
def updateOrder(request,pk):
    
    order = Order.objects.get(id=pk)
    form = OrderForm()
    
    if request.method == 'POST':
        # print('Printing POST:',request.POST)
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form':form}
    return render(request,'accounts/order_form.html',context)


@login_required(login_url='login')
@admin_only
def deleteOrder(request,pk):
    
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('order')
        
    context = {'item':order}
    return render(request,'accounts/delete.html',context)