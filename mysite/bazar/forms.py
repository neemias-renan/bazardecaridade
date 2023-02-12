from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CharityEvent, Item

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.EmailInput(attrs={'class': 'custom-input form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'custom-input form-control'}))

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'custom-input form-control'}))    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'custom-input form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'custom-input form-control'}))
    
class ItemForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea)
    photo = forms.ImageField()
    price = forms.FloatField()

class CreateEventForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input form-control'}))
    start_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input form-control'}))
    end_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input form-control'}))
    class Meta:
        model = CharityEvent
        fields = ['name', 'description', 'start_date', 'end_date']