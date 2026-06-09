from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'customer', 'amount', 'payment_method', 'status', 'verified_by_backend', 'created_at']
    list_filter = ['status', 'payment_method', 'verified_by_backend']
    search_fields = ['order__id', 'customer__username', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Payment Information', {'fields': ('order', 'customer', 'amount', 'payment_method')}),
        ('Status & Security', {'fields': ('status', 'transaction_id', 'verified_by_backend')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

    actions = ['verify_selected_payments']

    def verify_selected_payments(self, request, queryset):
        queryset.update(verified_by_backend=True, status='completed')
        self.message_user(request, "Selected payments verified successfully.")