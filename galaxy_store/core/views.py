from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def home(request):
    prods = Prod.objects.all()
    if request.GET.get('search'):
        search = request.GET.get('search')
        prods = Prod.objects.filter(
        Q(hname__icontains = search)|
        Q(hdesc__icontains = search)
        )
        
    return render(request, 'index.html',{'prods':prods})



def products(request):
    search = request.GET.get('search')
    
    if search:
        prods = Prod.objects.filter(
            Q(pname__icontains=search) |
            Q(pdesc__icontains=search)
        )
    else:
        prods = Prod.objects.all()




    # Sort products by newest first
    prods = prods.order_by('-created_at')

    # Group products by category (new categories will appear first)
    grouped = {}
    for prod in prods:
        cat = prod.category
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(prod)

    return render(request, 'prods.html', {'grouped': grouped})



def prod_details(request, id):
    prod = get_object_or_404(Prod, id=id)
    return render(request, 'prod_details.html', {'prod':prod})


def booking(request):
    prods = Prod.objects.all()
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        datetime = request.POST.get('datetime')
        destination = request.POST.get('destination')
        message = request.POST.get('message')

        user = ProdBooking.objects.filter(email=email, user=request.user)
        if user.exists():
            messages.info(request, 'Email is already use')
            return redirect('booking')

        user = ProdBooking.objects.create(
            user=request.user,
            fullname=fullname,
            email=email,
            phone=phone,
            address=address,
            # Assuming datetime is a valid DateTimeField input
            datetime=datetime,
            destination=destination,
            message=message,
        )
        
        user.save()
        messages.success(request, 'Your Hotel is Book successfullly')
        return redirect('yourprod')

    return render(request, 'booking.html', {'prods':prods})


def update_booking(request, id):
    prods = Prod.objects.all()
    booking = get_object_or_404(ProdBooking, id=id)

    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        destination = request.POST.get('destination')
        message = request.POST.get('message')

        booking.fullname = fullname
        booking.email = email
        booking.address = address
        booking.destination = destination
        booking.message = message

        booking.save()

        messages.success(request, 'Booking Updated Successfully.')
        return redirect('yourprod')

    return render(request, 'update_booking.html', {'booking':booking, 'prods':prods})


def delete_booking(request, id):
    booking = get_object_or_404(ProdBooking, id=id)
    
    if request.method == "POST":
        booking.delete()
        messages.success(request, 'Your booking has been deleted successfully')
        return redirect('yourprod')

    return render(request, 'delete_booking.html', {'booking':booking})



def yourprod(request):
    prodbook = ProdBooking.objects.filter(user=request.user)
    return render(request, 'yourhotel.html',{'prodbook':prodbook})


def contact(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')


        user = Contact.objects.create(
            fullname=fullname,
            email=email,
            subject=subject,
            message=message
        )

        user.save()
        messages.success(request, 'Your message successfullly send')
        return redirect('contact')

    return render(request, 'contact.html')

@login_required
def your_products(request):
    if request.method == "POST":
        pname = request.POST.get("pname")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        category = request.POST.get("category")

        # Product create
        product = Prod.objects.create(
            user=request.user,
            pname=pname,
            price=price,
            stock=stock,
            category=category,
        )

        # Multiple images add
        images = request.FILES.getlist("images")
        for img in images:
            Prod_Image.objects.create(prod=product, image=img)

        messages.success(request, "Product added successfully!")
        return redirect("your_products")

    products = Prod.objects.filter(user=request.user)
     # categories nikalna
    categories = Prod.objects.values_list("category", flat=True).distinct()

    # category wise products (dictionary banane ke liye)
    category_products = {}
    for cat in categories:
        category_products[cat] = Prod.objects.filter(category=cat).order_by("-created_at")
    
    return render(request, "your_product.html", {"products": products, "category_products": category_products})


# ✏️ Edit product
@login_required
def edit_product(request, pk):
    product = get_object_or_404(Prod, pk=pk, user=request.user)

    if request.method == "POST":
        product.pname = request.POST.get("pname")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.category = request.POST.get("category")
        product.save()

        # Nayi images add karne ka option
        images = request.FILES.getlist("images")
        for img in images:
            Prod_Image.objects.create(prod=product, image=img)

        messages.success(request, "Product updated successfully!")
        return redirect("your_products")

    return render(request, "edit_product.html", {"product": product})


# ❌ Delete product
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Prod, pk=pk, user=request.user)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect("your_products")