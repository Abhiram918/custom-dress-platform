from django.urls import path
from . import views

urlpatterns = [
    path('mine/', views.my_orders, name='my_orders'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/update/', views.update_order_status, name='update_order_status'),
    path('<int:pk>/alteration/', views.request_alteration, name='request_alteration'),
    path('<int:pk>/alteration-response/', views.handle_alteration_response, name='handle_alteration_response'),
]
