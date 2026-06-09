import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment
from orders.models import Order
from designers.models import DesignerDesign
from dress_requests.models import DressRequest

@login_required
def buy_now(request, design_id):
    if request.user.user_type != 'customer':
        messages.error(request, "Only customers can purchase designs.")
        return redirect('designer_list')
        
    design = get_object_or_404(DesignerDesign, pk=design_id)
    if request.method == 'POST':
        method = request.POST.get('payment_method')
        # Card Validation
        if method == 'card':
            if not re.fullmatch(r'\d{16}', request.POST.get('card_number', '').replace(' ', '')):
                messages.error(request, "Invalid Card Number.")
                return render(request, 'payments/confirm_purchase.html', {'design': design})

        # Create records
        req = DressRequest.objects.create(
            customer=request.user, designer=design.designer, dress_type=design.category,
            status='accepted', quoted_price=design.price_estimate,
            bust=request.POST.get('bust'), waist=request.POST.get('waist'),
            hips=request.POST.get('hips'), height=request.POST.get('height')
        )
        order = Order.objects.create(
            customer=request.user, designer=design.designer, dress_request=req,
            final_price=design.price_estimate, shipping_address=request.POST.get('address'),
            status='paid' if method == 'card' else 'pending'
        )
        Payment.objects.create(
            order=order, customer=request.user, amount=order.final_price,
            payment_method=method, status='completed' if method == 'card' else 'pending',
            verified_by_backend=(method == 'card')
        )
        return redirect('payment_success', order_id=order.id)
    return render(request, 'payments/confirm_purchase.html', {'design': design})

@login_required
def create_checkout_session(request, request_id):
    dress_request = get_object_or_404(DressRequest, pk=request_id, customer=request.user)
    
    if dress_request.status != 'accepted':
        messages.error(request, "This request is not ready for payment.")
        return redirect('my_requests')

    if hasattr(dress_request, 'order'):
        return redirect('order_detail', pk=dress_request.order.pk)

    if request.method == 'POST':
        method = request.POST.get('payment_method')
        address = request.POST.get('address')
        
        if not address:
            messages.error(request, "Please provide a shipping address.")
            return render(request, 'payments/confirm_commission_purchase.html', {'dress_request': dress_request})

        # Card Validation
        if method == 'card':
            if not re.fullmatch(r'\d{16}', request.POST.get('card_number', '').replace(' ', '')):
                messages.error(request, "Invalid Card Number.")
                return render(request, 'payments/confirm_commission_purchase.html', {'dress_request': dress_request})

        # Create order
        order = Order.objects.create(
            customer=request.user,
            designer=dress_request.designer,
            dress_request=dress_request,
            final_price=dress_request.quoted_price,
            shipping_address=address,
            status='paid' if method == 'card' else 'accepted'
        )
        
        # Create payment record
        Payment.objects.create(
            order=order,
            customer=request.user,
            amount=order.final_price,
            payment_method=method,
            status='completed' if method == 'card' else 'pending',
            verified_by_backend=(method == 'card')
        )
        
        messages.success(request, "Payment successful! Your order is now being processed.")
        return redirect('payment_success', order_id=order.id)
        
    return render(request, 'payments/confirm_commission_purchase.html', {'dress_request': dress_request})


@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'payments/success.html', {'order': order})