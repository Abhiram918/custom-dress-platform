from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DressRequest
from .forms import DressRequestForm
from designers.models import DesignerProfile


@login_required
def create_request(request, designer_id):
    if request.user.user_type != 'customer':
        messages.error(request, "Only customers can request custom designs.")
        return redirect('designer_list')
        
    designer = get_object_or_404(DesignerProfile, pk=designer_id)
    design_id = request.GET.get('design')
    initial_data = {}
    
    if design_id:
        from designers.models import DesignerDesign
        design = get_object_or_404(DesignerDesign, pk=design_id)
        initial_data = {
            'dress_type': design.category,
            'description': f"I am interested in a piece similar to your design: '{design.title}'.\n\n[Ref: {design.pk}]",
            'budget': design.price_estimate
        }
    
    if request.method == 'POST':
        form = DressRequestForm(request.POST, request.FILES)
        if form.is_valid():
            dress_request = form.save(commit=False)
            dress_request.customer = request.user
            dress_request.designer = designer
            dress_request.save()
            messages.success(request, f"Your request has been sent to {designer.business_name}!")
            return redirect('my_requests')
    else:
        form = DressRequestForm(initial=initial_data)
        
    return render(request, 'dress_requests/create.html', {
        'form': form,
        'designer': designer
    })


@login_required
def my_requests(request):
    if request.user.user_type == 'designer':
        requests = DressRequest.objects.filter(designer__user=request.user)
    else:
        requests = DressRequest.objects.filter(customer=request.user)
    return render(request, 'dress_requests/my_requests.html', {'requests': requests})


@login_required
def request_detail(request, pk):
    dress_request = get_object_or_404(DressRequest, pk=pk)
    
    # Security: Only customer or designer can view
    customer_name = dress_request.customer.get_full_name() or dress_request.customer.username
    designer_specialty = dress_request.designer.get_specialties_display()
    return render(request, 'dress_requests/detail.html', {
        'dress_request': dress_request,
        'customer_name': customer_name,
        'designer_specialty': designer_specialty
    })


@login_required
def respond_to_request(request, pk):
    dress_request = get_object_or_404(DressRequest, pk=pk)
    
    # Security: Only the designer can respond
    if request.user.user_type != 'designer' or request.user != dress_request.designer.user:
        messages.error(request, "Only the assigned designer can respond to this request.")
        return redirect('home')

    if request.method == 'POST':
        status = request.POST.get('status')
        notes = request.POST.get('designer_notes')
        price = request.POST.get('quoted_price')
        completion = request.POST.get('estimated_completion')
        
        if status in ['accepted', 'declined']:
            dress_request.status = status
            dress_request.designer_notes = notes
            if status == 'accepted':
                if not price:
                    messages.error(request, "Please provide a quoted price.")
                    return redirect('request_detail', pk=pk)
                dress_request.quoted_price = price
                dress_request.estimated_completion = completion
            
            dress_request.save()
            messages.success(request, f"Request {status} successfully.")
            return redirect('request_detail', pk=pk)
            
    return redirect('request_detail', pk=pk)
