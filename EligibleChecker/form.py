from django import forms
from .models import  CustomUser
from django.core.exceptions import ValidationError
import re


class CreateCustomUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    username = forms.CharField(max_length=150, required=True, help_text="Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only.")
    class Meta:
        model=CustomUser
        fields=['username','email',  'password1', 'password2']


    def clean_password2(self):
    
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password1):  # At least one uppercase letter
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password1):  # At least one lowercase letter
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password1):  # At least one digit
            raise forms.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[@#$%^&+=_.]', password1):  # At least one special character
            raise forms.ValidationError("Password must contain at least one special character (e.g., @, #, $, %, ^).")
        
        return password2
        
    
    def clean_email(self):
        # Ensure email is unique
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Email address must end with '@gmail.com'.")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
    
        if not re.match(r'^[a-zA-Z0-9@.+_-]+$', username):  # Ensure username has valid characters
            raise forms.ValidationError("Username can only contain letters, digits, and @/./+/-/_ characters.")
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

