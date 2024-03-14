from django.shortcuts import render, redirect
from login_app.models import *
from user_app.models import ProductDetails
from django.contrib import messages
from main.settings import BASE_DIR
import os

STATIC_DIR = os.path.join(BASE_DIR, 'seller_app', 'static', 'images')

# Create your views here.
def dashboard(request):
    user = request.user
    if not user or not user.is_staff:
        return redirect('login')
    admin_details = AdminDetails.objects.filter(user=user).first()
    products = ProductDetails.objects.filter(publisher=user).all()
    return render(request, 'dashboard.html', {'admin': admin_details,
                                              'products': products})

def manage_products(request):
    user = request.user
    if not user or not user.is_staff:
        return redirect('login')
    products = ProductDetails.objects.filter(publisher=user).all()
    return render(request, 'manage_products.html', {'products': products})

def handle_uploaded_file(file):
    with open(os.path.join(STATIC_DIR, file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def add_product(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST['name']
        desc = request.POST['desc']
        price = request.POST['price']
        img = request.FILES['img']
        handle_uploaded_file(img)
        product = ProductDetails(name=name, description=desc, price=price, publisher=user, file_name=img.name)
        product.save()
        return render(request, 'add_products.html', {"stats": "Product Added Successfully"})

    return render(request, 'add_products.html')

def manage(request, id):
    product = ProductDetails.objects.filter(id=id).first()
    file_name = 'images/'+product.file_name
    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['desc']
        price = request.POST['price']
        product = ProductDetails.objects.filter(id=id).first()
        product.name = name
        product.description = desc
        product.price = price
        try:
            img = request.FILES['img']
            handle_uploaded_file(img)
            product.file_name = img.name
            file_name = 'images/'+product.file_name
        except:
            product.save()
        product.save()
    return render(request, 'manage.html', {'product': product,
                                           'file_name': file_name
                                           })

def delete_product(request, id):
    product = ProductDetails.objects.filter(id=id).first()
    product.delete()
    return redirect('manage_products')

def profile(request):
    user = request.user
    user_details = AdminDetails.objects.filter(user=user).first()
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        store = request.POST['store_name']
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user_details.phone_number = phone
        user_details.address = address
        user_details.store_name = store
        user.save()
        user_details.save()
        messages.success(request, "Profile Updated Successfully")

    return render(request, 'profile.html', {'user':user,
                                            'user_details': user_details})


