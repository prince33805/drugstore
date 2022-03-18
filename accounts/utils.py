import json
from .models import *

def cookieCart(request):

	#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0,'shipping':True}
	cartItems = order['get_cart_items']	
 
	for i in cart:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:	
			if(cart[i]['quantity']>0): #items with negative quantity = lot of freebies  
				cartItems += cart[i]['quantity']

				product = Product.objects.get(id=i)
				total = (product.price * cart[i]['quantity'])

				order['get_cart_total'] += total
				order['get_cart_items'] += cart[i]['quantity']
    
				item = {
					'product':{
						'id':product.id,
						'name':product.name,
						'price':product.price,
						'imageURL':product.imageURL
						},
					'quantity':cart[i]['quantity'],
					'get_total':total,
					}
				items.append(item)
		except:
			pass
    
	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
    # giving the same code as cart, bcz same, total data will be rendered in frontend
    if request.user.is_authenticated:
        customer = request.user.customer
        # get_or_create is used to search for a qiven object,
        # and, if it isn't there, it then creates tht model object
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # the below line, is used to query from the OrderItem model
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        
    else:
        # cookieCart function is present in utils.py, and to use it, it's imported here
        # check utils.py for cookieCart function
        cookieData = cookieCart(request)
        # cookieData is a dictionary
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems, 'order':order, 'items':items}
