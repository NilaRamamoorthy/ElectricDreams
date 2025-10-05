from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    phone_number = forms.CharField(max_length=15)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password != confirm:
            raise forms.ValidationError("Passwords do not match")

        phone = cleaned_data.get('phone_number')
        if Profile.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("Phone number already registered")

        return cleaned_data
