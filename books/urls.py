from django.urls import path
from . import views
urlpatterns = [
    path('', views.book_list, name='item_list'),
    path('book/<int:pk>/', views.book_detail, name='item_detail'),
    path('accounts/signup', views.sign_up, name='signup'),
    path('add-to-cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart, name='remove_from_cart'),
    path('order-summary', views.order_summary, name='order-summary'),
    path('checkout', views.checkout, name='checkout'),
    path('payment/<payment_option>/', views.payment, name='payment'),
    path('payment/stripe/status/success', views.payment_success, name='payment_success'),
    path('payment/stripe/status/failed', views.payment_failed, name='payment_failed')
]