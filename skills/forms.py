import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SkillPost, Review, Appointment


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class SkillPostForm(forms.ModelForm):
    class Meta:
        model = SkillPost
        fields = ['title', 'category', 'description', 'rate', 'contact', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'rate': 'Rate / Trade',
            'contact': 'Contact Info',
            'is_active': 'Listing is active',
        }
        help_texts = {
            'rate': 'e.g. Free, $15/hr, Trade for coffee',
            'contact': 'Email, phone, or how to reach you',
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'message': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Any details for the skill provider? (optional)'}),
        }
        labels = {
            'message': 'Note (optional)',
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError("Please choose a date in the future.")
        return date


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')]
            ),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your experience...'}),
        }
        labels = {
            'comment': 'Your Review',
        }
