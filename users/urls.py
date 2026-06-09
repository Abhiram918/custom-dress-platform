from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile_update'),
    path('profile/delete/', views.profile_delete_view, name='profile_delete'),
    path('password/change/', views.change_password_view, name='change_password'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user/toggle/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('order/update-status/<int:order_id>/', views.update_order_status, name='admin_update_order_status'),
    path('designer/approve/<int:user_id>/', views.approve_designer, name='approve_designer'),
    path('designer/reject/<int:user_id>/', views.reject_designer, name='reject_designer'),
]
