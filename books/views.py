from django.shortcuts import render
from django.http import HttpResponse
from .models import Author, BookItem, OrderItem, Order, BillingAddress, Payment
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from . import forms
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import stripe

stripe.api_key = 'your key'


# Create your views here.
def book_list(request):
    items = BookItem.objects.all()
    return render(request, 'index.html', context={'items': items})

def book_detail(request, pk):
    try:
        item = BookItem.objects.get(pk=pk)
        return render(request, 'item_detail.html', context={'item': item})

    except ObjectDoesNotExist:
        print('object doesn\'t exists')

def sign_up(request):

    if request.method == 'POST':
        form = forms.SignUp(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                word = form.cleaned_data['word']
                word2 = form.cleaned_data['word2']
                if word != word2:
                    messages.add_message(request, messages.ERROR, 'words didn\'t match.')
                    return redirect('signup')
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                if User.objects.get(email=email):
                    messages.add_message(request, messages.ERROR, 'User with this email already exists')
                    return redirect('signup')
                else:                
                    user = User.objects.create_user(username=username, word=word, email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    messages.add_message(request, messages.SUCCESS, 'Sign up success')
                    return redirect('login')
            except IntegrityError:
                messages.add_message(request, messages.ERROR, 'Username already exists.')
                return redirect('signup')
        else:
            messages.add_message(request, messages.ERROR, 'INVALID FORM')
            return redirect('signup')
    else:
        form = forms.SignUp()
        return render(request, 'signup.html', context={'form': form})

@login_required()
def add_to_cart(request, pk):
    item = get_object_or_404(BookItem, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(user=request.user, ordered=False, item=item)
    try:
        order_obj = Order.objects.get(user=request.user, ordered=False)
    except ObjectDoesNotExist:
        order_obj = None
    if order_obj:
        if order_obj.order_items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect('item_detail', pk=pk)
        else:
            order_item.quantity = 1
            order_obj.order_items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect('item_detail', pk=pk)
    else:
        start_order_date = timezone.now()
        order_obj = Order.objects.create(user=request.user, ordered=False, start_date=start_order_date)
        order_obj.order_items.add(order_item)
        order_obj.save()
        messages.info(request, "Your order was created and the item was added to your cart.")
        return redirect('item_detail', pk=pk)

@login_required()
def remove_from_cart(request, pk):
    item = get_object_or_404(BookItem, pk=pk)
    try:
        order_item = OrderItem.objects.get(user=request.user, ordered=False, item=item)
    except ObjectDoesNotExist:
        messages.info(request, "This item wasn't in your order items")
        return redirect('item_detail', pk=pk)
    try:
        order_obj = Order.objects.get(user=request.user, ordered=False)
    except ObjectDoesNotExist:
        order_obj = None
    if order_obj:
        try:
            order_obj.order_items.get(item=item) #OrderItem.objects.filter(user=request.user, ordered=False, item=item, pk=pk)
            order_obj.order_items.remove(order_item)
            order_item.quantity = 1
            order_item.save()
            messages.info(request, "Item successfuly removed from cart")
            return redirect('item_detail', pk=pk)
        except ObjectDoesNotExist:
            messages.info(request, "This item wasn't in your cart.")
            return redirect('item_detail', pk=pk)
    else:
        messages.info(request, "You don't have an active order.")
        return redirect('item_detail', pk=pk)

@login_required()
def order_summary(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        return render(request, 'order_summary.html', context={'order': order})

    except ObjectDoesNotExist:
        messages.info(request, "You don't have an active order.")
        return redirect('item_list')

@login_required()
def checkout(request):

    if request.method == 'GET':
        form = forms.Checkout()
        #print(form)
        return render(request, 'checkout.html', context={'form': form})
    else:
        form = forms.Checkout(request.POST)
        try:
            order = Order.objects.get(user=request.user, ordered=False)        
            if form.is_valid():
                print('Valid form!!')               
                shipping_address = form.cleaned_data['shipping_address']
                country = form.cleaned_data['country']
                zip = form.cleaned_data['zip']
                billing_address = BillingAddress(user=request.user, shipping_address=shipping_address, country=country, zip_code=zip)
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                if form.cleaned_data['payment_option'] == 'S':
                    return redirect('payment', payment_option='stripe')
                if form.cleaned_data['payment_option'] == 'P':
                    return redirect('payment', payment_option='paypal')
        except ObjectDoesNotExist:
            messages.error(request, 'You do not have an active order!')
            return redirect('item_list')

@login_required()
def payment(request, payment_option):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
    except ObjectDoesNotExist:
        messages.error(request, 'You do not have an active order!')
    amount = int(order.get_total()*100)
    intent = stripe.PaymentIntent.create(amount=amount, currency='usd')
    payment, created = Payment.objects.get_or_create(user=request.user, amount=order.get_total(), option=payment_option)
    context = {'client_secret': intent.client_secret}
    return render(request, 'payment.html', context=context)


@login_required()
def payment_success(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        #order.payment = Payment.
    except ObjectDoesNotExist:
        messages.error(request, 'You do not have an active order!')

    payment = Payment.objects.get(user=request.user, pending=True)
    payment.pending = False
    payment.status = 'S'
    payment.save()

    order.payment = payment
    order.ordered = True
    order.save()
    return render(request, 'payment_success.html')

@login_required()
def payment_failed(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        #order.payment = Payment.
    except ObjectDoesNotExist:
        messages.error(request, 'You do not have an active order!')

    payment = Payment.objects.get(user=request.user, pending=True)
    payment.pending = False
    payment.status = 'F'
    payment.save()

    return render(request, 'payment_failed.html')
