from django.urls import path
from . import views

urlpatterns = [
    path('', views.designer_list, name='designer_list'),
    path('dashboard/', views.designer_dashboard, name='designer_dashboard'),
    path('upload/', views.upload_design, name='upload_design'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('<int:pk>/', views.designer_detail, name='designer_detail'),
    path('review/<int:order_id>/', views.submit_review, name='submit_review'),
    path('design/edit/<int:design_id>/', views.edit_design, name='edit_design'),
    path('design/delete/<int:design_id>/', views.delete_design, name='delete_design'),
]
