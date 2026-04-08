from django import forms
from .models import ForumPost, ForumReply, Feedback


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'category', 'body', 'post_anonymously']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Discussion title'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'body': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 8,
                'placeholder': 'Start the discussion...'
            }),
        }


class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ['body', 'post_anonymously']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 5,
                'placeholder': 'Write your reply...'
            }),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your name (optional)'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Your email (optional)'}),
            'subject': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What is this about?'}),
            'message': forms.Textarea(attrs={'class': 'form-input', 'rows': 6, 'placeholder': 'Tell us what you think, report a bug, or suggest an improvement...'}),
        }