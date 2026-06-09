from django.db import models
from django.conf import settings


class DesignerProfile(models.Model):
    """
    Designer profile linked to a User account.
    Contains professional information about the designer.
    """
    SPECIALTY_CHOICES = (
        ('wedding', 'Wedding Dresses'),
        ('casual', 'Casual Wear'),
        ('evening', 'Evening Wear'),
        ('formal', 'Formal Wear'),
        ('traditional', 'Traditional Wear'),
        ('custom', 'Custom Designs'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    )
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='designer_profile'
    )
    business_name = models.CharField(max_length=200)
    bio = models.TextField()
    specialties = models.CharField(
        max_length=50,
        choices=SPECIALTY_CHOICES,
        default='custom'
    )
    experience_years = models.PositiveIntegerField(default=0)
    price_range_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Minimum price in currency"
    )
    price_range_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Maximum price in currency"
    )
    portfolio_images = models.JSONField(
        default=list,
        blank=True,
        help_text="List of portfolio image URLs"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        help_text="Average rating from reviews"
    )
    total_orders = models.PositiveIntegerField(default=0)
    total_earnings = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Whether designer is accepting new requests"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.business_name} - {self.user.username}"
    
    class Meta:
        ordering = ['-rating', '-total_orders']


class DesignerDesign(models.Model):
    """
    Specific dress designs uploaded by designers to showcase their work.
    Shown on the home page and in the designer's portfolio.
    """
    designer = models.ForeignKey(
        DesignerProfile,
        on_delete=models.CASCADE,
        related_name='designs'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='designs/')
    category = models.CharField(
        max_length=50,
        choices=DesignerProfile.SPECIALTY_CHOICES,
        default='custom'
    )
    price_estimate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Starting price for this design"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.designer.business_name}"

    class Meta:
        ordering = ['-created_at']
