from django.db import models
from django.conf import settings


class Order(models.Model):
    """
    Confirmed order after request acceptance and payment.
    Tracks the complete lifecycle of a dress order.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('paid', 'Paid'),
        ('in_progress', 'Tailoring'),
        ('ready', 'Ready'),
        ('shipped', 'Shipping'),
        ('delivered', 'Delivered'),
        ('altering', 'Altering'),
        ('completed', 'Done'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )
    
    # Valid status transitions
    VALID_TRANSITIONS = {
        'pending': ['accepted', 'cancelled'],
        'accepted': ['paid', 'in_progress', 'cancelled'],
        'paid': ['in_progress', 'refunded'],
        'in_progress': ['ready', 'cancelled'],
        'ready': ['shipped'],
        'shipped': ['delivered'],
        'delivered': ['completed', 'altering'],
        'altering': ['ready', 'shipped'],
        'completed': ['altering'],
        'cancelled': [],
        'refunded': [],
    }
    
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_orders'
    )
    designer = models.ForeignKey(
        'designers.DesignerProfile',
        on_delete=models.CASCADE,
        related_name='designer_orders'
    )
    dress_request = models.OneToOneField(
        'dress_requests.DressRequest',
        on_delete=models.CASCADE,
        related_name='order'
    )
    
    order_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )
    
    final_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Final agreed price"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Tracking information
    tracking_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    shipping_address = models.TextField()
    
    # Progress notes
    progress_notes = models.TextField(
        blank=True,
        help_text="Designer's progress updates"
    )
    
    # Completion
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Delivery timestamp – used for the 7-day alteration window
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Generate order number if not exists
        if not self.order_number:
            import uuid
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        # Set delivered_at when order is first delivered
        if self.status == 'delivered' and not self.delivered_at:
            from django.utils import timezone
            self.delivered_at = timezone.now()
        
        # Set completed_at if status becomes completed
        if self.status == 'completed' and not self.completed_at:
            from django.utils import timezone
            self.completed_at = timezone.now()
            # Also increment designer's total order count
            self.designer.total_orders += 1
            self.designer.save()
            
        # If order was being altered and is now delivered/completed, mark alteration as done
        if self.status in ('delivered', 'completed') and hasattr(self, 'alteration_request'):
            alteration = self.alteration_request
            if alteration.status == 'accepted':
                alteration.status = 'completed'
                alteration.save()

        super().save(*args, **kwargs)
    
    def can_transition_to(self, new_status):
        """Check if status transition is valid"""
        return new_status in self.VALID_TRANSITIONS.get(self.status, [])
    
    def __str__(self):
        return f"Order {self.order_number} - {self.customer.username}"
    
    class Meta:
        ordering = ['-created_at']

    @property
    def is_cod(self):
        """Check if this order is Cash on Delivery."""
        return hasattr(self, 'payment') and self.payment.payment_method == 'cod'

    def alteration_window_open(self):
        """Returns True if within the 7-day alteration window after delivery."""
        if self.delivered_at:
            from django.utils import timezone
            return (timezone.now() - self.delivered_at).days < 7
        return False


class AlterationRequest(models.Model):
    """Customer request to alter a delivered order within 7 days."""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='alteration_request'
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='alteration_requests'
    )
    description = models.TextField(
        help_text="Describe the alterations needed"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    designer_notes = models.TextField(
        blank=True,
        help_text="Designer's response / notes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Alteration for {self.order.order_number} – {self.status}"

    class Meta:
        ordering = ['-created_at']
