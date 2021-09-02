from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Category,Product,Cart,Addresses,CartItem,Order

def home(request):
    object_list = ['Men','Women','Boys','Girls']
    return render(request,'store/home.html',{'object_list':object_list})

def category(request, text):
    queryset = Category.objects.filter(meant_for = text)
    prices = [499, 799, 999] if text in ['Men', 'Women'] else [299, 499, 699]
    return render(request,'store/category.html',{'queryset': queryset, 'text': text, 'prices': prices})

def productlist(request,text,product):
    queryset = Product.objects.filter(category__meant_for = text)
    
    if product != '0':
        queryset = queryset.filter(category__name = product)
    
    if request.GET.get('price', None):
        filter_price = request.GET.get('price', None)
        queryset = queryset.filter(price__lte = filter_price)

    paginator = Paginator(queryset, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 

    return render(request,'store/productlist.html',{'page_obj': page_obj, 'paginator': paginator})

def productdetail(request,id):
    object=Product.objects.get(id=id)
    return render(request,'store/productdetail.html',{'object':object})

@login_required
def addtocart(request,ID,size):
    product = Product.objects.get(id = ID)

    if len(Cart.objects.filter(user__id = request.user.id).filter(ordered = False)) == 0:
        cart = Cart(user = request.user)
        cart.save()
    else:
        cart = Cart.objects.filter(user__id = request.user.id).filter(ordered = False)[0]

    for item in cart.cartitem_set.all():
        if item.product.id == product.id and item.size == size:
            messages.add_message(request, messages.INFO, 'Item already in cart.')
            return redirect(f'/product/{product.id}')
    
    cart_item = CartItem(product = product, size = size, quantity = 1, cart = cart)
    cart_item.save()
    cart.cartitem_set.add(cart_item)
    messages.add_message(request, messages.INFO, 'Item added to cart.')
    return redirect(f'/product/{product.id}')

@login_required
def yourcart(request):
    cart = Cart.objects.filter(user__id = request.user.id).filter(ordered = False)
    if len(cart) > 0 and len(cart[0].cartitem_set.all()) > 0:
        cart = cart[0]
        bill_amount = 0
        for item in cart.cartitem_set.all():
            if item.quantity > item.product.size_inventory[item.size]:
                item.quantity = item.product.size_inventory[item.size]
                if item.quantity == 0: 
                    messages.add_message(request, messages.INFO, f'Requested quantity unavailable for {item.product.name} ({item.size}). Item out of stock.')
                    item.delete()
                else: 
                    messages.add_message(request, messages.INFO, f'Requested quantity unavailable for {item.product.name} ({item.size}). Available quantity: {item.product.size_inventory[item.size]} ')
                    item.save()
            bill_amount += (item.product.price * item.quantity)
        return render(request, 'store/cart.html', {'cart_items': list(cart.cartitem_set.all()), 'bill_amount': bill_amount})
    else:
        messages.add_message(request, messages.INFO, 'Cart is empty.')
        return render(request, 'store/cart.html', )

@login_required
def deletefromcart(request, id):
    cart_item = CartItem.objects.get(id = id)
    cart_id = cart_item.cart.id
    cart_item.delete()
    if len(Cart.objects.get(id = cart_id).cartitem_set.all()) == 0:
        cart = Cart.objects.get(id = cart_id)
        cart.delete()
        
    return redirect('/yourCart/')
    
@login_required
def incquantity(request, item_id):
    cart_item = CartItem.objects.get(id = item_id)
    available_stock = cart_item.product.size_inventory[cart_item.size]

    if cart_item.quantity + 1 <= available_stock:
        cart_item.quantity += 1
        cart_item.save()
    else:
        messages.add_message(request, messages.WARNING, 'Requested quantity unavailable')
    return redirect('/yourCart/')

@login_required
def decquantity(request,item_id):
    cart_item = CartItem.objects.get(id = item_id)
    if cart_item.quantity == 1:
        return redirect(f'/deleteFromCart/{item_id}')
    cart_item.quantity -= 1
    cart_item.save()
    return redirect('/yourCart/')

@login_required
def add_address(request):
    if request.method == 'GET':
        return render(request, 'store/addaddress.html')

    elif request.method == 'POST':
        street_building = request.POST['street_building']
        area = request.POST['area']
        city = request.POST['city']
        phone = request.POST['phone']
        pin = request.POST['pin']
        address = Addresses(user = request.user, street_building = street_building, area = area, city = city, phone = phone, pin = pin)
        address.save()
        messages.add_message(request, messages.INFO, 'Address added successfully.')
        return redirect('/checkout/')

@login_required
def checkout(request):
    if request.method == 'GET':
        if len(Cart.objects.filter(user=request.user).filter(ordered=False)) == 0:
            length = len(Cart.objects.filter(user=request.user).filter(ordered=False))
            messages.add_message(request, messages.INFO, 'Cart is empty. Continue Shopping!')
            return render(request, 'store/checkout.html', {'render': False})

        cart = Cart.objects.filter(user = request.user).filter(ordered = False)[0]
        total_bill = 0

        for item in cart.cartitem_set.all():
            if item.quantity > item.product.size_inventory[item.size]:
                item.quantity = item.product.size_inventory[item.size]
                item.save()
                messages.add_message(request, messages.INFO, f'Requested quantity unavailable for {item.product.name}. Available quantity: {item.quantity}')
            total_bill += (item.product.price * item.quantity)

        user_addresses = Addresses.objects.filter(user = request.user)
        return render(request, 'store/checkout.html', {'addresses': user_addresses, 'bill_amount': total_bill, 'render': True, 'cart_items': list(cart.cartitem_set.all())})

    elif request.method == 'POST':
        address_id = request.POST['address']
        address = Addresses.objects.get(id = address_id)
        cart = Cart.objects.filter(user = request.user).filter(ordered = False)[0]
        cart.ordered = True
        
        bill_amount = 0 
        for item in cart.cartitem_set.all():
            item.ordered_price = item.product.price
            item.save()
            bill_amount += (item.ordered_price * item.quantity)
        
        
        order = Order(cart = cart, bill_amount = bill_amount, address = address, status = 'processing')
        order.save()
        cart.save()
        
        messages.add_message(request, messages.INFO, 'Order placed successfully!')
        return redirect('/')
    
@login_required
def orderlist(request):
    orders = Order.objects.filter(cart__user = request.user)
    return render(request, 'store/orders.html', {'orders' : orders})

@login_required
def orderdetail(request, id):
    order = Order.objects.get(id = id)
    if order.cart.user == request.user:
        return render(request, 'store/orderdetail.html', {'order': order})
    messages.add_message(request, messages.INFO, 'Order ID is of another user.')
    return redirect('/orders/')

@login_required
def cancelorder(request, orderid):
    order = Order.objects.get(id = orderid)
    if order.cart.user == request.user:
        order.status = 'cancelled'
        order.save()
        messages.add_message(request, messages.INFO, f'Order: {orderid} has been cancelled.')
    else:
        messages.add_message(request, messages.INFO, 'This order was not placed from your account.')
    return redirect('/orders/')

@login_required
def addresslist(request):
    addresses = Addresses.objects.filter(user = request.user)
    return render(request, 'store/addresses.html', {'addresses': addresses})

@login_required
def deleteaddress(request, addressid):
    address = Addresses.objects.get(id = addressid)
    if address.user == request.user:
        address.delete()
        messages.add_message(request, messages.INFO, 'Address Deleted.')
    else:
        messages.add_message(request, messages.INFO, 'Address could not be deleted.')
    return redirect('/addresses/')

