from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product, Customer, Cart, Order, OrderItem
from django.db.models import Count, Q
from .forms import CustomerRegForm, CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
import stripe
from django.conf import settings
from django.urls import reverse
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def home(request):
    return render(request, 'shop/home.html', locals())


class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        titles = product.values('title').annotate(total=Count('title'))
        return render(request, 'shop/category.html', locals())
    

class CategoryTitleView(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        titles = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'shop/category.html', locals())
    

class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        return render(request, 'shop/product_detail.html', locals())


class CustomerRegisterView(View):

    def get(self, request):
        form = CustomerRegForm()
        return render(request, 'shop/customer_reg.html', locals())

    def post(self, request):
        form = CustomerRegForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulation, your profile is created')
        else:
            messages.error(request, 'Invalid, what is happened')

        return render(request, 'shop/customer_reg.html', locals())


class ProfileView(View):

    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'shop/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            number = form.cleaned_data['number']
            new_customer = Customer(user=user, name=name, locality=locality, city=city, number=number, zipcode=zipcode, state=state)
            new_customer.save()
            messages.success(request, 'Congratulation, Profile save successfulled!')
        else:
            messages.error(request, 'Invalid Profile.')
        return render(request, 'shop/profile.html', locals())


class AddressView(View):
    def get(self, request):
        add = Customer.objects.filter(user=request.user)
        return render(request, 'shop/address.html', locals())

class updateProfileView(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'shop/update_profile.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.zipcode = form.cleaned_data['zipcode']
            add.state = form.cleaned_data['state']
            add.number = form.cleaned_data['number']
            add.save()
            messages.success(request, 'Congratulation, Profile save successfulled!')
        else:
            messages.error(request, 'Invalid Profile.')
        return redirect('shop:address')


# Add to cart view
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('shop:cart')

#Show cart vue
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    total = len(cart)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discount_price
        amount += value
    totalamount = amount + 40
    return render(request, 'shop/cart.html', locals())

#checkout view
class CheckoutView(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0
        for p in cart_items:
            value = p.quantity * p.product.discount_price
            amount += value
        totalamount = amount + 40
        return render(request, 'shop/checkout.html', locals())

    def post(self, request):
        user = request.user
        add_id = request.POST.get('custid')
        customer = Customer.objects.filter(user=user)
        add = customer.get(id=add_id)
       
        cart = Cart.objects.filter(user=user)
        order = Order.objects.create(user=user, customer=add)
        order.save()
        amount = 0
        for item in cart:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            value = item.quantity * item.product.discount_price
            amount += value
        totalamount = amount + 40
        request.session['order_id'] = order.id
        cart.delete()
        return redirect(reverse('shop:process'))

def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for item in cart:
        value = item.quantity * item.product.discount_price
        amount += value
    totalamount = amount + 40
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('shop:sucess'))
        cancel_url = request.build_absolute_uri(reverse('shop:cancel'))
        session_data = {
            'mode': 'payment',
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.product.discount_price * 100),
                    'currency': 'usd',
                    'product_data': {
                    'name': item.product.title,
                    }
                },
                'quantity': item.quantity,
                })
        # Ajouter une ligne pour les frais d'expédition
        session_data['line_items'].append({
            'price_data': {
                'unit_amount': 4000,  # Le prix de 40 euros en cents
                'currency': 'usd',    # La devise utilisée pour les frais d'expédition
                'product_data': {
                    'name': 'Frais d\'expédition',
                },
            },
            'quantity': 1,
        })
        #create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)
    else:
        return render(request, 'shop/process.html', locals())


# Increment quantity
def pluscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount += value
        totalamount = amount + 40

        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount

        }
        return JsonResponse(data)

#Decrement quantity
def minuscart(request):
    if  request.method == "GET":
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=user))
        if c.quantity > 1:
            c.quantity -= 1
        c.save()
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount += value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
            'deleted': False
        }
        return JsonResponse(data)

# Remove items
def removecart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount += value
        totalamount = amount + 40

        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount

        }
        return JsonResponse(data)


def payment_success(request):
    return render(request, 'shop/completed.html')


def payment_cancel(request):
    return render(request, 'shop/canceled.html')
