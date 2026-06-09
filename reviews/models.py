from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """
    Customer reviews for completed orders.
    Can only be created after order is completed.
    """
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_given'
    )
    designer = models.ForeignKey(
        'designers.DesignerProfile',
        on_delete=models.CASCADE,
        related_name='reviews_received'
    )
    order = models.OneToOneField(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='review'
    )
    
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    
    review_text = models.TextField(
        blank=True,
        help_text="Written review"
    )
    
    # Review images
    review_images = models.JSONField(
        default=list,
        blank=True,
        help_text="Images of the completed dress"
    )
    
    # Designer response
    designer_response = models.TextField(
        blank=True,
        help_text="Designer's response to the review"
    )
    responded_at = models.DateTimeField(null=True, blank=True)
    
    is_verified = models.BooleanField(
        default=False,
        help_text="Whether the review is verified by admin"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Review by {self.customer.username} for {self.designer.business_name} - {self.rating} stars"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update designer's average rating
        self.update_designer_rating()
    
    def update_designer_rating(self):
        """Update designer's average rating"""
        from django.db.models import Avg
        avg_rating = Review.objects.filter(
            designer=self.designer
        ).aggregate(Avg('rating'))['rating__avg']
        
        if avg_rating:
            self.designer.rating = round(avg_rating, 2)
            self.designer.save()
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['customer', 'order']
