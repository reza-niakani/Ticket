from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Ticket,Answer


class UserLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput (attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class UserRegisterForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput (attrs={'class':'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='confrim password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Using Django Validator to check the existence of the desired email

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email is exists')
        return email

    # Using Django Validator to check the existence of the desired username

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('this username is exist')
        return username

    # Using Django validation to compare the sameness of two input passwords
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('your passwords must be match')


class TiketForm(forms.ModelForm):
    class Meta:
        model=Ticket
        fields=('title','body')
        widgets={
            'body':forms.Textarea(attrs={'class':'form-control'})
        }

class AnswerMessageForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': ' write your text',
            }),
        }
        labels = {
            'body': 'answer',
        }


