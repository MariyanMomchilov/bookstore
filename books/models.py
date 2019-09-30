from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

#import math

# Create your models here.



class BookItem(models.Model):
    BOOK_GENRE_CHOICES = [
        ('aaa', 'Action and adventure'),
        ('ah', 'Alternate history'),
        ('ath', 'Anthology'),
        ('cdr', 'Children\'s'),
        ('cbk', 'Comic book'),
        ('crm', 'Crime'),
        ('dra', 'Drama'),
        ('fai', 'Fairytale'),
        ('fan', 'Fantasy'),
        ('nov', 'Novel'),
        ('hif', 'Historical fiction'),
        ('hor', 'Horror'),
        ('mys', 'Mystery'),
        ('rom', 'Romance'),
        ('thr', 'Thriller'),
        ('poe', 'Poetry'),
        ('sat', 'Satire'),
        ('scf', 'Science fiction'),
        ('bio', 'Biography'),
        ('art', 'Art'),
        ('cok', 'Cookbook'),
        ('dia', 'Diary'),
        ('dic', 'Dictionary'),
        ('enc', 'Encyclopedia'),
        ('hea', 'Health'),
        ('his', 'History'),
        ('jou', 'Journal'),
        ('sci', 'Science'),
        ('seh', 'Self help'),
        ('prg', 'Programming'),
        ('bns', 'Business'),
    ]

    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=3, choices=BOOK_GENRE_CHOICES)
    authorr = models.ForeignKey('Author', on_delete=models.CASCADE, blank=True)
    description = models.TextField()
    price = models.FloatField()
    d_price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} from {self.authorr}"

class Author(models.Model):
    fname = models.CharField(max_length=30)
    mname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    info = models.TextField()
    books = models.ManyToManyField(BookItem, blank=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(BookItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity}/ {self.item}/ {self.user}'

    def get_item_cost(self):
        return self.item.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    order_items = models.ManyToManyField(OrderItem, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now=True)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f'{self.user}/ {self.ordered}'

    def get_total(self):
        total = 0
        for order_item in self.order_items.all():
            total += order_item.get_item_cost()
        return round(total, 2)

class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=200)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=30, default=None)

    def __str__(self):
        return f'{self.user} with {self.shipping_address}'

class Payment(models.Model):

    STATUS_CHOICES = (('S','SUCCESS'),
                     ('F', 'FAILED'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    option = models.CharField(max_length=10)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True, blank=True)
    pending = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user}'

