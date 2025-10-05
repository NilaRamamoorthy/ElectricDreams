from django import forms
from .models import ContactMessage, CallbackRequest

# Contact Page
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["first_name", "last_name", "phone", "email", "address", "message"]
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            "phone": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            "email": forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email id'}),
            "address": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            "message": forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Type your message...'}),
        }



# Emergency electrician
class CallbackRequestForm(forms.ModelForm):
    class Meta:
        model = CallbackRequest
        fields = ['name', 'mobile', 'email', 'services']

