from django import forms
from .models import DressRequest


class DressRequestForm(forms.ModelForm):
    class Meta:
        model = DressRequest
        fields = [
            'dress_type', 'description', 'budget', 'deadline',
            'bust', 'waist', 'hips', 'height', 'sleeve_length',
            'fabric_type', 'neck_type', 'hemline', 'preferred_color',
            'reference_photo'
        ]
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'preferred_color': forms.TextInput(attrs={'type': 'color', 'style': 'height: 45px;'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            if field in ['bust', 'waist', 'hips', 'height', 'sleeve_length']:
                self.fields[field].widget.attrs.update({'placeholder': 'Inches'})
