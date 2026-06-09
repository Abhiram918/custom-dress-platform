from django.contrib import admin
from .models import DressRequest


@admin.register(DressRequest)
class DressRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'customer',
        'designer',
        'dress_type',
        'status',
        'budget',
        'quoted_price',
        'created_at'
    ]
    list_filter = ['status', 'dress_type', 'created_at']
    search_fields = ['customer__username', 'designer__business_name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Request Details', {
            'fields': ('customer', 'designer', 'dress_type', 'description', 'reference_images')
        }),
        ('Measurements', {
            'fields': ('bust', 'waist', 'hips', 'height', 'additional_measurements')
        }),
        ('Budget & Timeline', {
            'fields': ('budget', 'deadline')
        }),
        ('Designer Response', {
            'fields': ('status', 'designer_notes', 'quoted_price', 'estimated_completion')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
