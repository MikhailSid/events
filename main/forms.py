from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Location, Place, Event
from django.forms import ModelForm, TextInput, Select, DateTimeInput, NumberInput, Textarea

class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'password1', 'password2')

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['name']
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название локации'
            })}
        
class PlaceForm(ModelForm):
    class Meta:
        model = Place
        fields = ['location', 'name', 'description']
        widgets = {
            "location": Select(attrs={
                'class': 'form-control'
            }),
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название места'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание места'
            })}
        
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['place', 'name', 'description', 'date_start', 'date_end']
        widgets = {
            "place": Select(attrs={
                'class': 'form-control'
            }),
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название события'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание события'
            }),
            "date_start": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата и время начала'
            }),
            "date_end": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата и время окончания'
            })}