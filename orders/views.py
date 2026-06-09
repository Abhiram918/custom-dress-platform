from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Order, AlterationRequest


@login_required
def my_orders(request):
    if request.user.user_type == 'designer':
        orders = Order.objects.filter(designer__user=request.user)
    else:
        orders = Order.objects.filter(customer=request.user)
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    # Security: Allow admin, customer, and designer
    if not (request.user.is_superuser or request.user.user_type == 'admin' or 
            request.user == order.customer or request.user == order.designer.user):
        messages.error(request, "Access denied.")
        return redirect('home')
        
    return render(request, 'orders/detail.html', {
        'order': order,
        'order_statuses': Order.STATUS_CHOICES,
        'alteration_window_open': order.alteration_window_open(),
    })


@login_required
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    # Security: Designer and Admin can update
    is_admin = request.user.is_superuser or request.user.user_type == 'admin'
    if not (is_admin or request.user == order.designer.user):
        messages.error(request, "Only the designer or admin can update order status.")
        return redirect('order_detail', pk=pk)
        
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('progress_notes')
        
        # Rule Enforcement based on user role
        if not is_admin:
            # Designer restrictions
            if new_status == 'delivered':
                messages.error(request, "Only administrators can mark an order as delivered.")
                return redirect('order_detail', pk=pk)
            if order.status == 'shipped' and new_status != 'shipped':
                messages.error(request, "Please wait for admin to confirm delivery.")
                return redirect('order_detail', pk=pk)
            if new_status == 'completed' and order.status != 'delivered' and order.status != 'altering':
                messages.error(request, "Order must be delivered before it can be closed.")
                return redirect('order_detail', pk=pk)
        else:
            # Admin restrictions
            if new_status == 'delivered' and order.status != 'shipped':
                messages.error(request, "Delivery can only be confirmed once the order is shipped.")
                return redirect('order_detail', pk=pk)
            
            # Allow 'delivered' and 'cancelled' for admins
            if new_status not in ['delivered', 'cancelled'] and not request.user.is_superuser:
                messages.warning(request, "Administrators only confirm delivery or cancel orders.")
                return redirect('order_detail', pk=pk)

        # Check transition if not superuser
        if request.user.is_superuser or order.can_transition_to(new_status):
            order.status = new_status
            if notes:
                order.progress_notes = notes
            order.save()
            messages.success(request, f"Order status updated to {new_status}.")
        else:
            messages.error(request, f"Invalid status transition from {order.status} to {new_status}.")
            
    # Redirect back to where they came from
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('order_detail', pk=pk)


@login_required
def request_alteration(request, pk):
    order = get_object_or_404(Order, pk=pk)

    # Only the customer of this order can request alteration
    if request.user != order.customer:
        messages.error(request, "Only the customer of this order can request alterations.")
        return redirect('order_detail', pk=pk)

    # Order must be delivered or completed
    if order.status not in ('delivered', 'completed'):
        messages.error(request, "Alterations can only be requested for delivered orders.")
        return redirect('order_detail', pk=pk)

    # Enforce 7-day window
    if not order.alteration_window_open():
        messages.error(request, "The 7-day alteration window has closed for this order.")
        return redirect('order_detail', pk=pk)

    # Prevent duplicate requests
    if hasattr(order, 'alteration_request'):
        messages.warning(request, "You have already submitted an alteration request for this order.")
        return redirect('order_detail', pk=pk)

    if request.method == 'POST':
        description = request.POST.get('description', '').strip()
        if not description:
            messages.error(request, "Please describe the alterations you need.")
            return redirect('order_detail', pk=pk)

        AlterationRequest.objects.create(
            order=order,
            customer=request.user,
            description=description,
        )
        messages.success(request, "Alteration request submitted! The designer will be in touch.")
        return redirect('order_detail', pk=pk)

    return redirect('order_detail', pk=pk)
@login_required
def handle_alteration_response(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    # Only the designer or admin can handle alteration responses
    is_admin = request.user.is_superuser or request.user.user_type == 'admin'
    if not (is_admin or request.user == order.designer.user):
        messages.error(request, "Only the designer or admin can handle alteration requests.")
        return redirect('order_detail', pk=pk)

    if not hasattr(order, 'alteration_request'):
        messages.error(request, "No alteration request found for this order.")
        return redirect('order_detail', pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        notes = request.POST.get('designer_notes', '').strip()
        
        alteration = order.alteration_request
        alteration.designer_notes = notes
        
        if action == 'accept':
            alteration.status = 'accepted'
            # Move order status back to a state that allows re-delivery
            # We use 'altering' status which we just added
            order.status = 'altering'
            order.save()
            messages.success(request, "Alteration request accepted. Order status updated to 'Altering'.")
        elif action == 'reject':
            alteration.status = 'rejected'
            messages.info(request, "Alteration request rejected.")
        
        alteration.save()
        
    return redirect('order_detail', pk=pk)
