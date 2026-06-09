from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('user/<int:user_id>/', views.conversation, name='conversation'),
    path('request/<int:request_id>/', views.conversation_by_request, name='conversation_request'),
    path('order/<int:order_id>/', views.conversation_by_order, name='conversation_order'),
]
