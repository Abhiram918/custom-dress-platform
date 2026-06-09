from django.db import models
from django.conf import settings


class Message(models.Model):
    """
    Messaging system for communication between customers and designers.
    Supports threaded conversations linked to requests or orders.
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    
    # Optional: Link to request or order
    dress_request = models.ForeignKey(
        'dress_requests.DressRequest',
        on_delete=models.CASCADE,
        related_name='messages',
        null=True,
        blank=True
    )
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='messages',
        null=True,
        blank=True
    )
    
    message_text = models.TextField()
    
    # Attachments (images, files)
    attachments = models.JSONField(
        default=list,
        blank=True,
        help_text="List of attachment URLs"
    )
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"
    
    class Meta:
        ordering = ['created_at']
