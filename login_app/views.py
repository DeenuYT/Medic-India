from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from .utils import mail, validate
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
import tensorflow as tf
from keras.models import load_model
import numpy as np
import pandas as pd
import os
from main.settings import BASE_DIR

labels = ['Aloevera', 'Amla', 'Amruthaballi', 'Arali', 'Astma_weed', 'Badipala', 'Balloon_Vine', 'Bamboo', 'Beans', 'Betel', 'Bhrami', 'Bringaraja', 'Caricature', 'Castor', 'Catharanthus', 'Chakte', 'Chilly', 'Citron lime (herelikai)', 'Coffee', 'Common rue(naagdalli)', 'Coriender', 'Curry', 'Doddpathre', 'Drumstick', 'Ekka', 'Eucalyptus', 'Ganigale', 'Ganike', 'Gasagase', 'Ginger', 'Globe Amarnath', 'Guava', 'Henna', 'Hibiscus', 'Honge', 'Insulin', 'Jackfruit', 'Jasmine', 'Kambajala', 'Kasambruga', 'Kohlrabi', 'Lantana', 'Lemon', 'Lemongrass', 'Malabar_Nut', 'Malabar_Spinach', 'Mango', 'Marigold', 'Mint', 'Neem', 'Nelavembu', 'Nerale', 'Nooni', 'Onion', 'Padri', 'Palak(Spinach)', 'Papaya', 'Parijatha', 'Pea', 'Pepper', 'Pomoegranate', 'Pumpkin', 'Raddish', 'Rose', 'Sampige', 'Sapota', 'Seethaashoka', 'Seethapala', 'Spinach1', 'Tamarind', 'Taro', 'Tecoma', 'Thumbe', 'Tomato', 'Tulsi', 'Turmeric', 'ashoka', 'camphor', 'kamakasturi', 'kepala']
STATIC_DIR = os.path.join(BASE_DIR, 'seller_app', 'static')

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):

    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        passw = request.POST['pass']
        cpassw = request.POST['cpass']
        
        if User.objects.filter(email=email):
            messages.warning(request, "Email already exists!")
            return render(request, 'signup.html')

        if passw != cpassw:
            messages.warning(request, "Passwords mismatch!")
            return render(request, 'signup.html')
        
        if not validate.validate_email(email):
            messages.warning(request, "Invalid Email")
            return render(request, 'signup.html')
        
        elif not validate.validate_password(passw):
            messages.warning(request, "Create a Strong password")
            return render(request, 'signup.html')

        user = User.objects.create_user(email=email, password=passw, username=fname+lname, first_name=fname, last_name=lname)
        user.is_active = False
        user.save()

        user_details = UserDetails(phone_number=phone, address=address, user=user)
        user_details.save()

        mail.welcome_mail(request, user, email=email, passw=passw)
        mail.verification_email(request, user)

        return render(request, 'verify_account.html')
        
    return render(request, 'signup.html')

def create_seller(request):
    if request.method == 'POST':

        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        store = request.POST['store_name']
        passw = request.POST['pass']
        cpassw = request.POST['cpass']

        if User.objects.filter(email=email):
            messages.warning(request, "Email already exists!")
            return render(request, 'create_seller.html')

        if passw != cpassw:
            messages.warning(request, "Passwords mismatch!")
            return render(request, 'create_seller.html')
        
        if not validate.validate_email(email):
            messages.warning(request, "Invalid Email")
            return render(request, 'create_seller.html')
        
        elif not validate.validate_password(passw):
            messages.warning(request, "Create a Strong password")
            return render(request, 'create_seller.html')
        
        user = User.objects.create_user(email=email, password=passw, username=fname+lname, first_name=fname, last_name=lname)
        user.is_active = False
        user.save()

        user_details = AdminDetails(phone_number=phone, address=address, user=user, store_name=store)
        user_details.save()

        return render(request, 'seller_creation_request.html', {'name': fname})
    
    return render(request, 'create_seller.html')

def login_(request):

    if request.method == 'POST':
        email = request.POST['email']
        passw = request.POST['pass']

        if not User.objects.filter(email=email):
                messages.warning(request, "Email not found! Create an account")
                return render(request, 'login.html')
        
        user = authenticate(request, email=email, password=passw)

        if user:
            if user.is_active and not user.is_staff:
                login(request, user)
                return redirect('home')
            elif user.is_active and user.is_staff:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.warning(request, "Please activate your account!")
                return render(request, "login.html")
        else:
            messages.error(request, "Enter valid email and password!!")
            return render(request, "login.html")
        
    return render(request, 'login.html')

def logout_(request):

    if request.user:
        logout(request)
        return redirect('login')
    
def activate(request, uidb64, token):
    
    user = get_object_or_404(get_user_model(), pk=force_str(urlsafe_base64_decode(uidb64)))

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'verify_successful.html')
    
def medic_tools(request):
    return render(request, 'medic_tools.html')

def chatbot(request):
    return render(request, 'chatbot.html')

def handle_uploaded_file(file):
    with open(os.path.join(STATIC_DIR, file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def predict(request):
    if request.method == 'POST':
        model = load_model(os.path.join(BASE_DIR, 'login_app', 'model_80_classes.h5'))
        img = request.FILES['img']
        handle_uploaded_file(img)
        filename = img.name
        img = tf.keras.preprocessing.image.load_img(os.path.join(BASE_DIR, 'seller_app', 'static', img.name), target_size=(299, 299))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        predictions = model.predict(img_array)
        score = tf.nn.sigmoid(predictions[0])
        pred_cls = labels[np.argmax(score)]
        data = pd.read_csv(os.path.join(BASE_DIR, 'login_app', 'leaf_info_utf.csv'))
        data = data.sort_values('Plant Name')
        data = data = data.iloc[np.argmax(score)]
        name = data[1]
        uses = data[2].split('/')
        chars = data[3].split('/')
        return render(request, 'prediction_results.html', {
            'name': name,
            'uses': uses,
            'chars': chars,
            'img': f'{filename}',
        })
    return render(request, 'plant_predictions.html')

def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')