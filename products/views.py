from django.shortcuts import render, redirect
from .forms import ProductForm
from django.contrib import messages
from .models import Product

import requests
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
import json
from .credentials import *


def products(request):
    all_products = Product.objects.all()
    context = {"products": all_products}
    return render(request, 'products/products.html', context)


def add_products(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product=form.save(commit=False)
            product.owner=request.user
            form.save()
            messages.success(request, 'Product saved successfully')
            return redirect("add-products-url")
        else:
            messages.error(request, 'Product saving failed')
            return redirect("add-products-url")
    else:
        form = ProductForm()
    return render(request, 'products/add-products.html', {'form': form})


def update_products(request, id):
    product = Product.objects.get(id=id)
    if request.user !=product.owner:
        return redirect('products-url')
    if request.method == "POST":
        product_name = request.POST.get('name')
        product_qtty = request.POST.get('qtty')
        product_price = request.POST.get('price')
        product_desc = request.POST.get('desc')
        product_image = request.FILES.get('image')
        product.name = product_name
        product.qtty = product_qtty
        product.price = product_price
        product.desc = product_desc
        product.image = product_image
        product.save()
        messages.success(request, 'Product updated successfully')
        return redirect('products-url')
    return render(request, 'products/update-products.html', {'product': product})


def delete(request, id):
    product = Product.objects.get(id=id)
    if request.user !=product.owner:
        return redirect('products-url')
    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect('products-url')


def pay(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        phone = request.POST['phone']
        amount = product.price
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
            "Password": LipanaMpesaPassword.decode_password,
            "Timestamp": LipanaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "PYMENT001",
            "TransactionDesc": "School fees"
        }

        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse('Success')
    return render(request, 'products/pay.html', {'product': product})
