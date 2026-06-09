from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'sender',
        'receiver',
        'dress_request',
        'order',
        'is_read',
        'created_at'
    ]
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'receiver__username', 'message_text']
    readonly_fields = ['created_at', 'read_at']
    
    fieldsets = (
        ('Message Details', {
            'fields': ('sender', 'receiver', 'message_text', 'attachments')
        }),
        ('Context', {
            'fields': ('dress_request', 'order')
        }),
        ('Status', {
            'fields': ('is_read', 'read_at')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
