from django import forms
from .models import TripReport, ReportComment


class TripReportForm(forms.ModelForm):
    class Meta:
        model = TripReport
        fields = [
            'title', 'destination', 'post_anonymously',
            'trip_start', 'trip_end', 'travel_style',
            'body', 'tips', 'safety_rating',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Give your report a descriptive title'}),
            'destination': forms.Select(attrs={'class': 'form-input'}),
            'trip_start': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'trip_end': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'travel_style': forms.Select(attrs={'class': 'form-input'}),
            'body': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 15,
                'placeholder': 'Share your experience — route, logistics, encounters, what surprised you...'
            }),
            'tips': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 5,
                'placeholder': 'Key tips you wish you had known before going'
            }),
            'safety_rating': forms.Select(attrs={'class': 'form-input'}),
        }

    def clean_body(self):
        body = self.cleaned_data.get('body', '')
        if len(body) > 50000:
            raise forms.ValidationError("Report body cannot exceed 50,000 characters.")
        return body


class ReportCommentForm(forms.ModelForm):
    class Meta:
        model = ReportComment
        fields = ['body', 'post_anonymously']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 4,
                'placeholder': 'Ask a question or share your thoughts...'
            }),
        }
