from django.contrib import admin
from .models import Order, AlterationRequest


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number',
        'customer',
        'designer',
        'status',
        'final_price',
        'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'customer__username', 'designer__business_name']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'completed_at', 'delivered_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'designer', 'dress_request', 'final_price')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'tracking_number', 'shipping_address')
        }),
        ('Progress', {
            'fields': ('progress_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at', 'delivered_at')
        }),
    )
    
    actions = ['mark_as_shipped', 'mark_as_delivered', 'mark_as_completed']
    
    def mark_as_shipped(self, request, queryset):
        count = 0
        for order in queryset:
            if order.can_transition_to('shipped'):
                order.status = 'shipped'
                order.save()
                count += 1
        self.message_user(request, f"{count} order(s) marked as shipped.")
    mark_as_shipped.short_description = "Mark as Shipped"
    
    def mark_as_delivered(self, request, queryset):
        count = 0
        for order in queryset:
            if order.can_transition_to('delivered'):
                order.status = 'delivered'
                order.save()
                count += 1
        self.message_user(request, f"{count} order(s) marked as delivered.")
    mark_as_delivered.short_description = "Mark as Delivered"
    
    def mark_as_completed(self, request, queryset):
        from django.utils import timezone
        count = 0
        for order in queryset:
            if order.can_transition_to('completed'):
                order.status = 'completed'
                order.completed_at = timezone.now()
                order.save()
                count += 1
        self.message_user(request, f"{count} order(s) marked as completed.")
    mark_as_completed.short_description = "Mark as Completed"


@admin.register(AlterationRequest)
class AlterationRequestAdmin(admin.ModelAdmin):
    list_display = ['order', 'customer', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order__order_number', 'customer__username']
    readonly_fields = ['order', 'customer', 'description', 'created_at', 'updated_at']
    fields = ['order', 'customer', 'description', 'status', 'designer_notes', 'created_at', 'updated_at']
