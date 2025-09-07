from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import UserImage, UserProfile

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('login')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('login')

        else:
            login(request, user)
            return redirect('your_products')

    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        fullname = request.POST.get('fullname')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        discription = request.POST.get('description')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')


        user = User.objects.filter(username=email)
        if user.exists():
            messages.info(request, 'Email is already taken')
            return redirect('register')
        
        user = User.objects.create(
            username=email,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            fullname=fullname,
            mobile=mobile,
            address=address,
            description=discription
)

        user.set_password(password)
        user.save()

        # Image save in UserImage model
        user_image, created = UserImage.objects.get_or_create(user=user)
        user_image.image = image
        user_image.save()

        messages.success(request, 'Your account created successfully')
        return redirect('your_products')



    return render(request, 'register.html')

def logout_page(request):
    logout(request)
    return redirect('login')