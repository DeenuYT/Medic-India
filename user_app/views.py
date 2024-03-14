import stripe
from django.shortcuts import get_object_or_404, render, redirect
from .models import ProductDetails, Collections
from main.settings import STRIPE_SECRET_KEY
from login_app.models import AdminDetails, UserDetails
from django.contrib import messages

stripe.api_key = STRIPE_SECRET_KEY

# Create your views here.
def home(request):
    products = ProductDetails.objects.all()
    user_details = AdminDetails.objects.all()
    data = []
    for i in products:
        cont = {'id': i.id,
                'name': i.name,
                'description': i.description,
                'price': i.price,
                'file_name': 'images/'+i.file_name,
                'seller': user_details.filter(user=i.publisher).first().store_name
                }
        data.append(cont)
    return render(request, 'home.html', {'products': data})

def single_product(request, id):
    product = ProductDetails.objects.filter(id=id).first()
    user_details = AdminDetails.objects.filter(user=product.publisher).first()
    file_name = 'images/'+product.file_name
    collections = Collections.objects.filter(product=product).first()
    return render(request, 'single_product.html', {'product': product,
                                                   'user_details': user_details,
                                                   'file_name': file_name,
                                                   'collections': collections
                                                   })

def user_profile(request):
    user = request.user
    user_details = UserDetails.objects.filter(user=user).first()
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user_details.phone_number = phone
        user_details.address = address
        user.save()
        user_details.save()
        messages.success(request, "Profile Updated Successfully")

    return render(request, 'user_profile.html', {'user':user,
                                            'user_details': user_details})

def collection(request):
    user = request.user
    collections = Collections.objects.filter(email=user.email).all()
    user_details = AdminDetails.objects.all()
    data = []
    for i in collections:
        cont = {'id': i.product.id,
                'name': i.product.name,
                'description': i.product.description,
                'price': i.product.price,
                'file_name': 'images/'+i.product.file_name,
                'seller': user_details.filter(user=i.product.publisher).first().store_name
                }
        data.append(cont)
    return render(request, 'collections.html', {'products': data})

def add_to_collection(request, id):
    product = ProductDetails.objects.filter(id=id).first()
    collections = Collections(email=request.user.email, product=product)
    collections.save()
    return redirect('home')

def remove_from_collection(request, id):
    product = ProductDetails.objects.filter(id=id).first()
    collections = Collections.objects.filter(email=request.user.email, product=product).first()
    collections.delete()
    return redirect('home')

def start_checkout(request):
    user = request.user
    user_details = UserDetails.objects.filter(user=user).first()
    address = user_details.address

    cart_contents = get_cart_contents(request, user.email)

    line_items = []
    for item in cart_contents:
        line_item = {
            'price_data': {
                'currency': 'inr',
                'unit_amount': int(item['item_total'] * 100),
                'product_data': {
                    'name': item['product'].name,
                    'description': item['product'].description,
                },
            }, 
            'quantity': item['quantity']
        }
        line_items.append(line_item)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        metadata={
            'product_id':str(item['product'].id),
            'email':request.user.email,
            'first_name':request.user.first_name,
            'address':address,
        },
        mode='payment',
        success_url=request.build_absolute_uri('/success'),
        cancel_url=request.build_absolute_uri('/cancel'),
    )

    return redirect(session.url)



def get_cart_contents(request, email):
    cart_items = Collections.objects.filter(email=email)
    cart_with_details = []

    for cart_item in cart_items:
        item_total = float(int(cart_item.product.price))

        item_details = {
            'product': cart_item.product,
            'quantity': 1,
            'item_total': item_total,
        }

        cart_with_details.append(item_details)

    return cart_with_details
