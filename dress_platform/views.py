from django.shortcuts import render
from designers.models import DesignerDesign, DesignerProfile


def home_view(request):
    featured_designs = DesignerDesign.objects.all()[:6]
    top_designers = DesignerProfile.objects.filter(status='approved').order_by('-rating')[:3]
    return render(request, 'home.html', {
        'featured_designs': featured_designs,
        'top_designers': top_designers
    })
