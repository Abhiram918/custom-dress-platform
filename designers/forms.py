from django import forms
from .models import DesignerDesign, DesignerProfile


class DesignerDesignForm(forms.ModelForm):
    class Meta:
        model = DesignerDesign
        fields = ['title', 'description', 'image', 'category', 'price_estimate']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class DesignerProfileForm(forms.ModelForm):
    class Meta:
        model = DesignerProfile
        fields = ['business_name', 'bio', 'specialties', 'experience_years', 'price_range_min', 'price_range_max', 'is_available']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
