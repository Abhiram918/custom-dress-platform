from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, CustomPasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from orders.models import Order
from payments.models import Payment
from users.models import User
from designers.models import DesignerProfile
from dress_requests.models import DressRequest


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if user.user_type == 'designer':
                # Designers must wait for admin approval
                user.is_approved = False
                user.is_active = False  # Prevent login until approved
                user.save()
                form.save_m2m()
                messages.info(
                    request,
                    "Your designer registration has been submitted! "
                    "An admin will review your request. You will be able to log in once approved."
                )
                return redirect('login')
            else:
                user.save()
                form.save_m2m()
                login(request, user)
                messages.success(request, f"Welcome, {user.username}! Your account has been created.")
                if user.user_type == 'admin':
                    return redirect('admin_dashboard')
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Block designers who haven't been approved yet
                if user.user_type == 'designer' and not user.is_approved:
                    messages.warning(
                        request,
                        "Your designer account is pending admin approval. "
                        "Please wait until an admin reviews your registration."
                    )
                    return redirect('login')
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                if user.is_superuser or user.user_type == 'admin':
                    return redirect('admin_dashboard')
                elif user.user_type == 'designer':
                    return redirect('designer_dashboard')
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})


@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })


@login_required
def profile_delete_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your profile has been deleted successfully.")
        return redirect('home')
    return render(request, 'users/profile_confirm_delete.html')


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'admin')
def admin_dashboard(request):
    # Stats
    total_users = User.objects.count()
    total_designers = DesignerProfile.objects.count()
    total_customers = User.objects.filter(user_type='customer').count()
    total_orders = Order.objects.count()
    total_revenue = Payment.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Table data
    all_users = User.objects.all().exclude(id=request.user.id).order_by('-created_at')
    all_orders = Order.objects.all().order_by('-created_at')
    recent_payments = Payment.objects.all().order_by('-created_at')[:10]
    all_designers = DesignerProfile.objects.all().order_by('-created_at')
    pending_requests = DressRequest.objects.filter(status='pending').order_by('-created_at')
    # Designers waiting for approval
    pending_designers = User.objects.filter(user_type='designer', is_approved=False).order_by('-created_at')
    
    context = {
        'total_users': total_users,
        'total_designers': total_designers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'all_users': all_users,
        'all_orders': all_orders,
        'recent_payments': recent_payments,
        'all_designers': all_designers,
        'pending_requests': pending_requests,
        'pending_designers': pending_designers,
        'order_statuses': Order.STATUS_CHOICES,
    }
    return render(request, 'users/admin_dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'admin')
def toggle_user_status(request, user_id):
    user_to_toggle = get_object_or_404(User, id=user_id)
    if not user_to_toggle.is_superuser:
        user_to_toggle.is_active = not user_to_toggle.is_active
        user_to_toggle.save()
        status = "unblocked" if user_to_toggle.is_active else "blocked"
        messages.success(request, f"User {user_to_toggle.username} has been {status}.")
    else:
        messages.error(request, "Cannot block a superuser.")
    return redirect('admin_dashboard')


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'admin')
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            # Enforce rule: Admin marks shipped as delivered or cancels
            if order.status == 'shipped' and new_status == 'delivered':
                order.status = new_status
                order.save()
                messages.success(request, f"Order {order.order_number} marked as Delivered.")
            elif new_status == 'cancelled':
                order.status = new_status
                order.save()
                messages.success(request, f"Order {order.order_number} has been Cancelled.")
            elif request.user.is_superuser:
                # Superusers keep full override
                order.status = new_status
                order.save()
                messages.success(request, f"Order {order.order_number} status updated to {order.get_status_display()}.")
            else:
                messages.warning(request, "Administrators primarily confirm delivery or cancel orders.")
    # Redirect back to where they came from
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('admin_dashboard')


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'admin')
def approve_designer(request, user_id):
    """Admin approves a pending designer registration."""
    designer_user = get_object_or_404(User, id=user_id, user_type='designer')
    designer_user.is_approved = True
    designer_user.is_active = True  # Allow login
    designer_user.save()
    messages.success(
        request,
        f"Designer '{designer_user.username}' has been approved and can now log in."
    )
    return redirect('admin_dashboard')


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'admin')
def reject_designer(request, user_id):
    """Admin rejects (deletes) a pending designer registration."""
    designer_user = get_object_or_404(User, id=user_id, user_type='designer')
    username = designer_user.username
    designer_user.delete()
    messages.warning(
        request,
        f"Designer registration for '{username}' has been rejected and removed."
    )
    return redirect('admin_dashboard')
