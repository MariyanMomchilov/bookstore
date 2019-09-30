from django.contrib import admin
from books.models import Author, BookItem, OrderItem, Order, BillingAddress, Payment

# Register your models here.
admin.site.register(Author)
admin.site.register(BookItem)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(BillingAddress)
admin.site.register(Payment)
