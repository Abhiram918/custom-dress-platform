from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:designer_id>/', views.create_request, name='create_request'),
    path('mine/', views.my_requests, name='my_requests'),
    path('<int:pk>/', views.request_detail, name='request_detail'),
    path('<int:pk>/respond/', views.respond_to_request, name='respond_to_request'),
]
