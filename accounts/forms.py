from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class EdgeTravelRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class EdgeTravelLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'bio', 'countries_visited', 'allow_anonymous_posts',
            'show_email', 'avatar', 'location', 'website'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-input'}),
            'countries_visited': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'website': forms.URLInput(attrs={'class': 'form-input'}),
        }
