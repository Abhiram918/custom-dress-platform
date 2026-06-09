from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Message
from dress_requests.models import DressRequest
from orders.models import Order
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def chat_list(request):
    # Get all unique users this user has messaged
    sent_to = Message.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received_from = Message.objects.filter(receiver=request.user).values_list('sender', flat=True)
    
    unique_user_ids = set(list(sent_to) + list(received_from))
    contacts = User.objects.filter(id__in=unique_user_ids)
    
    return render(request, 'messaging/chat_list.html', {'contacts': contacts})


@login_required
def conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    # Get context from URL params if available
    request_id = request.GET.get('request_id')
    order_id = request.GET.get('order_id')
    
    dress_request = None
    order = None
    
    if request_id:
        dress_request = get_object_or_404(DressRequest, id=request_id)
    if order_id:
        order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        text = request.POST.get('message_text')
        if text:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                message_text=text,
                dress_request=dress_request,
                order=order
            )
            # Stay on the same conversation
            return redirect(f"{request.path}?{request.GET.urlencode()}")

    # Filter messages between these two users
    chat_messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('created_at')
    
    # Mark incoming as read
    chat_messages.filter(receiver=request.user, is_read=False).update(is_read=True)
    
    return render(request, 'messaging/conversation.html', {
        'other_user': other_user,
        'chat_messages': chat_messages,
        'dress_request': dress_request,
        'order': order
    })


@login_required
def conversation_by_request(request, request_id):
    dress_request = get_object_or_404(DressRequest, id=request_id)
    # The "other" user is the designer if current is customer, vice-versa
    if request.user == dress_request.customer:
        other_user = dress_request.designer.user
    else:
        other_user = dress_request.customer
        
    return redirect(f"/messages/user/{other_user.id}/?request_id={request_id}")


@login_required
def conversation_by_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user == order.customer:
        other_user = order.designer.user
    else:
        other_user = order.customer
        
    return redirect(f"/messages/user/{other_user.id}/?order_id={order_id}")
