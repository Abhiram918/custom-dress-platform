from django.db import models
from django.conf import settings


class DressRequest(models.Model):
    """
    Custom dress design request from customer to designer.
    This is the proposal stage before an order is created.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('cancelled', 'Cancelled'),
    )
    
    DRESS_TYPE_CHOICES = (
        ('wedding', 'Wedding Dress'),
        ('evening', 'Evening Gown'),
        ('casual', 'Casual Dress'),
        ('formal', 'Formal Dress'),
        ('traditional', 'Traditional Dress'),
        ('other', 'Other'),
    )
    
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dress_requests'
    )
    designer = models.ForeignKey(
        'designers.DesignerProfile',
        on_delete=models.CASCADE,
        related_name='incoming_requests'
    )
    dress_type = models.CharField(
        max_length=20,
        choices=DRESS_TYPE_CHOICES,
        default='other'
    )
    description = models.TextField(
        help_text="Detailed description of the desired dress"
    )
    reference_images = models.JSONField(
        default=list,
        blank=True,
        help_text="List of reference/inspiration image URLs"
    )
    
    FABRIC_CHOICES = (
        ('cotton', 'Cotton'),
        ('linen', 'Linen'),
        ('silk', 'Silk'),
        ('velvet', 'Velvet'),
        ('wool', 'Wool'),
        ('polyester', 'Polyester'),
        ('other', 'Other'),
    )

    NECK_TYPE_CHOICES = (
        ('v-neck', 'V-Neck'),
        ('round', 'Round Neck'),
        ('square', 'Square Neck'),
        ('halter', 'Halter'),
        ('off-shoulder', 'Off-Shoulder'),
        ('boat', 'Boat Neck'),
        ('high', 'High Neck'),
        ('scoop', 'Scoop Neck'),
    )

    HEMLINE_CHOICES = (
        ('mini', 'Mini'),
        ('knee', 'Knee-length'),
        ('midi', 'Midi'),
        ('maxi', 'Maxi'),
        ('floor', 'Floor-length'),
        ('asymmetrical', 'Asymmetrical'),
        ('high-low', 'High-Low'),
    )

    # Measurements
    bust = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    waist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hips = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sleeve_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Preferences
    fabric_type = models.CharField(max_length=20, choices=FABRIC_CHOICES, default='cotton')
    neck_type = models.CharField(max_length=20, choices=NECK_TYPE_CHOICES, blank=True)
    hemline = models.CharField(max_length=20, choices=HEMLINE_CHOICES, blank=True)
    preferred_color = models.CharField(max_length=7, default='#ffffff', help_text="Hex color code")
    reference_photo = models.ImageField(upload_to='requests/photos/', null=True, blank=True, help_text="Upload a reference photo")

    additional_measurements = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional measurements as key-value pairs"
    )
    
    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Customer's budget for the dress"
    )
    deadline = models.DateField(
        null=True,
        blank=True,
        help_text="Desired completion date"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    designer_notes = models.TextField(
        blank=True,
        help_text="Designer's notes or response to the request"
    )
    quoted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Price quoted by designer"
    )
    estimated_completion = models.DateField(
        null=True,
        blank=True,
        help_text="Designer's estimated completion date"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Request #{self.id} - {self.customer.username} to {self.designer.business_name}"
    
    class Meta:
        ordering = ['-created_at']
