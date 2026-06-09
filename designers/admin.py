from django.contrib import admin
from .models import DesignerProfile


@admin.register(DesignerProfile)
class DesignerProfileAdmin(admin.ModelAdmin):
    list_display = [
        'business_name',
        'user',
        'specialties',
        'status',
        'rating',
        'total_orders',
        'is_available',
        'created_at'
    ]
    list_filter = ['status', 'specialties', 'is_available']
    search_fields = ['business_name', 'user__username', 'user__email']
    readonly_fields = ['rating', 'total_orders', 'total_earnings', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'business_name', 'bio', 'specialties', 'experience_years')
        }),
        ('Pricing', {
            'fields': ('price_range_min', 'price_range_max')
        }),
        ('Portfolio', {
            'fields': ('portfolio_images',)
        }),
        ('Status & Performance', {
            'fields': ('status', 'is_available', 'rating', 'total_orders', 'total_earnings')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['approve_designers', 'reject_designers', 'suspend_designers']
    
    def approve_designers(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} designer(s) approved.")
    approve_designers.short_description = "Approve selected designers"
    
    def reject_designers(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} designer(s) rejected.")
    reject_designers.short_description = "Reject selected designers"
    
    def suspend_designers(self, request, queryset):
        queryset.update(status='suspended', is_available=False)
        self.message_user(request, f"{queryset.count()} designer(s) suspended.")
    suspend_designers.short_description = "Suspend selected designers"
