import re

from django import forms
from django.contrib.auth.models import User
import requests


class SignUpForm(forms.Form):
    name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'enter your name',
        'class': 'form-control border-0 p-4'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'enter your email.',
        'class': 'form-control border-0 p-4'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'enter your password.',
        'class': 'form-control border-0 p-4'
    }), min_length=8,  # Minimum length constraint
                               max_length=50,  # Maximum length constraint
                               help_text='Password should be at least 8 characters long.')  # Help text for the field)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        api_url = f'https://localhost:7071/Teacher/email-check/{email}'
        response = requests.post(api_url, verify=False)
        user_exists = False
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11")
        print(response.status_code)
        if response.status_code == 400:
            user_exists = True

        if user_exists:
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).{8,15}$'
        correct = bool(re.match(pattern, password))
        if correct:
            return password
        else:
            raise forms.ValidationError('Password should contain lower case,upper case and special characters')


class SignInForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'enter your email.',
        'class': 'form-control border-0 p-4'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'enter your password.',
        'class': 'form-control border-0 p-4'
    }))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            url_str = "https://localhost:7071/Teacher/SignInWithEmail"
            try:
                response = requests.post(url_str, json={'email': email, 'password': password}, verify=False)
                print("**********************************************")
                print(response.status_code)
                if response.status_code == 200:
                    return cleaned_data
                else:
                    raise forms.ValidationError('Email or password is incorrect.')
            except requests.RequestException as e:
                raise forms.ValidationError(f'Request failed: {str(e)}')
        else:
            raise forms.ValidationError('Email and password are required.')


class CourseForm(forms.Form):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'id_description'}))
    objectives = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'id_objectives'}))
    image = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control-file',
            'id': 'id_image',
            'accept': 'image/*'  # Only allow image files
        })
    )


class VideoForm(forms.Form):
    video = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control-file',
            'id': 'id_video',
            'accept': 'video/*'
        })
    )
    title = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'id_title', 'placeholder': 'enter title of video'}))


class ExamForm(forms.Form):
    name = forms.CharField(required=True, max_length=200,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_name'}))
    subjects = forms.CharField(required=True,
                               widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'id_description'}))


class QuestionForm(forms.Form):
    question = forms.CharField(required=True, max_length=400, widget=forms.TextInput(attrs={
        'placeholder': 'enter the question.',
        'class': 'form-control border-0 p-4',
        'style': 'background-color: #dadada;'
    }))
    option1 = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'enter option 1.',
        'class': 'form-control border-0 p-4',
        'style': 'background-color: #dadada;'
    }))
    option2 = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'enter option 2.',
        'class': 'form-control border-0 p-4',
        'style': 'background-color: #dadada;'
    }))
    option3 = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'enter option 3.',
        'class': 'form-control border-0 p-4',
        'style': 'background-color: #dadada;'
    }))
    option4 = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'enter option 4.',
        'class': 'form-control border-0 p-4',
        'style': 'background-color: #dadada;'
    }))
    category = forms.ChoiceField(choices=[
        ('vocabulary', 'Vocabulary'),
        ('grammar', 'Grammar'),
        ('reading', 'Reading')
    ], widget=forms.Select(attrs={
        'style': 'background-color: #dadada; border: none; padding: 1rem; width: 100%;border-radius: 0.5rem;'
    }), initial='vocabulary')
