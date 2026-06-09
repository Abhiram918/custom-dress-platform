from django.urls import path
from . import views

urlpatterns = [
    # Main entry point for the purchase
    path('buy-now/<int:design_id>/', views.buy_now, name='buy_now'),
    path('checkout/<int:request_id>/', views.create_checkout_session, name='create_checkout_session'),
#     path('buy-now/<int:design_id>/', views.buy_now, name='buy_now'),
#     path('success/<int:request_id>/', views.payment_success, name='payment_success'),
#     path('cancel/', views.payment_cancel, name='payment_cancel'),
    
    # Success page (Matches the 'order_id' used in our updated views.py)
    path('success/<int:order_id>/', views.payment_success, name='payment_success'),
]