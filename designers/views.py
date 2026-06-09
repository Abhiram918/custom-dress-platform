from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DesignerProfile, DesignerDesign
from reviews.models import Review


@login_required
def submit_review(request, order_id):
    # Allow admin or the actual customer to submit review
    if request.user.is_superuser or request.user.user_type == 'admin':
        order = get_object_or_404(Order, pk=order_id)
    else:
        order = get_object_or_404(Order, pk=order_id, customer=request.user)
    
    if order.status not in ['delivered', 'completed']:
        messages.error(request, "You can only rate a designer after the order is delivered.")
        return redirect('order_detail', pk=order_id)
        
    if hasattr(order, 'review'):
        messages.error(request, "You have already reviewed this order.")
        return redirect('order_detail', pk=order_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('comment', '')
        
        Review.objects.create(
            designer=order.designer,
            customer=request.user,
            order=order,
            rating=rating,
            review_text=review_text
        )
        
        messages.success(request, "Thank you for your review!")
        return redirect('order_detail', pk=order_id)

    return redirect('order_detail', pk=order_id)
from .forms import DesignerDesignForm, DesignerProfileForm
from dress_requests.models import DressRequest
from orders.models import Order


def designer_list(request):
    designers = DesignerProfile.objects.filter(status='approved', is_available=True)
    return render(request, 'designers/list.html', {'designers': designers})


def designer_detail(request, pk):
    designer = get_object_or_404(DesignerProfile, pk=pk)
    designs = DesignerDesign.objects.filter(designer=designer)
    reviews = Review.objects.filter(designer=designer).order_by('-created_at')
    return render(request, 'designers/detail.html', {
        'designer': designer, 
        'designs': designs,
        'reviews': reviews
    })


@login_required
def designer_dashboard(request):
    if request.user.user_type != 'designer':
        messages.error(request, "Access restricted to designers.")
        return redirect('home')
        
    try:
        designer = DesignerProfile.objects.get(user=request.user)
    except DesignerProfile.DoesNotExist:
        messages.info(request, "Please complete your designer profile to access the dashboard.")
        return redirect('complete_profile')

    recent_requests = DressRequest.objects.filter(designer=designer).order_by('-created_at')[:5]
    recent_orders = Order.objects.filter(designer=designer).order_by('-created_at')[:5]
    my_designs = DesignerDesign.objects.filter(designer=designer)
    
    return render(request, 'designers/dashboard.html', {
        'designer': designer,
        'recent_requests': recent_requests,
        'recent_orders': recent_orders,
        'my_designs': my_designs
    })


@login_required
def complete_profile(request):
    if request.user.user_type != 'designer':
        return redirect('home')
    
    try:
        instance = DesignerProfile.objects.get(user=request.user)
    except DesignerProfile.DoesNotExist:
        instance = None

    if request.method == 'POST':
        form = DesignerProfileForm(request.POST, instance=instance)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.status = 'approved'  # Auto-approve for demo/dev purposes
            profile.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('designer_dashboard')
    else:
        form = DesignerProfileForm(instance=instance)
    
    return render(request, 'designers/complete_profile.html', {'form': form})


@login_required
def upload_design(request):
    if request.user.user_type != 'designer':
        messages.error(request, "Access restricted to designers.")
        return redirect('home')
        
    try:
        designer = DesignerProfile.objects.get(user=request.user)
    except DesignerProfile.DoesNotExist:
        messages.error(request, "Please complete your profile first.")
        return redirect('complete_profile')
    
    if request.method == 'POST':
        form = DesignerDesignForm(request.POST, request.FILES)
        if form.is_valid():
            design = form.save(commit=False)
            design.designer = designer
            design.save()
            messages.success(request, "Design uploaded successfully!")
            return redirect('designer_dashboard')
    else:
        form = DesignerDesignForm()
        
    return render(request, 'designers/upload_design.html', {'form': form})


@login_required
def edit_design(request, design_id):
    if request.user.user_type != 'designer':
        messages.error(request, "Access restricted to designers.")
        return redirect('home')
    
    design = get_object_or_404(DesignerDesign, pk=design_id, designer__user=request.user)
    
    if request.method == 'POST':
        form = DesignerDesignForm(request.POST, request.FILES, instance=design)
        if form.is_valid():
            form.save()
            messages.success(request, "Design updated successfully!")
            return redirect('designer_detail', pk=design.designer.pk)
    else:
        form = DesignerDesignForm(instance=design)
        
    return render(request, 'designers/upload_design.html', {'form': form, 'edit': True})


@login_required
def delete_design(request, design_id):
    if request.user.user_type != 'designer':
        messages.error(request, "Access restricted to designers.")
        return redirect('home')
    
    design = get_object_or_404(DesignerDesign, pk=design_id, designer__user=request.user)
    designer_pk = design.designer.pk
    design.delete()
    messages.success(request, "Design deleted successfully!")
    return redirect('designer_detail', pk=designer_pk)
