from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'customer',
        'designer',
        'order',
        'rating',
        'is_verified',
        'created_at'
    ]
    list_filter = ['rating', 'is_verified', 'created_at']
    search_fields = ['customer__username', 'designer__business_name', 'review_text']
    readonly_fields = ['created_at', 'updated_at', 'responded_at']
    
    fieldsets = (
        ('Review Details', {
            'fields': ('customer', 'designer', 'order', 'rating', 'review_text', 'review_images')
        }),
        ('Designer Response', {
            'fields': ('designer_response', 'responded_at')
        }),
        ('Verification', {
            'fields': ('is_verified',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['verify_reviews', 'unverify_reviews']
    
    def verify_reviews(self, request, queryset):
        count = queryset.update(is_verified=True)
        self.message_user(request, f"{count} review(s) verified.")
    verify_reviews.short_description = "Verify selected reviews"
    
    def unverify_reviews(self, request, queryset):
        count = queryset.update(is_verified=False)
        self.message_user(request, f"{count} review(s) unverified.")
    unverify_reviews.short_description = "Unverify selected reviews"
