from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('products/', products, name='products'),
    path('booking/', booking, name='booking'),
    path('contact/', contact, name='contact'),
    path('product/detail/<int:id>/', prod_details, name='prod_details'),
    path('your/product/', yourprod , name='yourprod'),
    path('update-booking/<int:id>/', update_booking, name='prod_booking'),
    path('delete-booking/<int:id>/', delete_booking, name='delete_booking'),
    path("your-products/", your_products, name="your_products"),
    path("edit-product/<int:pk>/", edit_product, name="edit_product"),
    path("delete-product/<int:pk>/", delete_product, name="delete_product"),
]

# Super user
# username = root
# password = root