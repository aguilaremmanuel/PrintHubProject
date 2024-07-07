from django import forms
from .models import *
from django.core.exceptions import ValidationError

class ShopSignupForm(forms.ModelForm):

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'id': 'formGroupExampleInput',
            'placeholder': 'Confirm Password',
        })
    )

    class Meta:
        model = Shop
        fields = ['shop_name', 'fullname', 'email', 'contact_no', 'password', 'date_registered']
        widgets = {
            'shop_name': forms.TextInput(attrs={
                            'class': 'form-control',
                            'id': 'formGroupExampleInput',
                            'placeholder': 'Enter Shop Name'}),
            'fullname': forms.TextInput(attrs={
                            'class': 'form-control', 
                            'id': 'formGroupExampleInput',
                            'placeholder': 'Owner\'s Name'}),
            'email': forms.EmailInput(attrs={
                            'class': 'form-control', 
                            'id': 'formGroupExampleInput',
                            'placeholder': 'Email'}),
            'contact_no': forms.TextInput(attrs={
                            'class': 'form-control', 
                            'id': 'formGroupExampleInput',
                            'placeholder': 'Contact Number'}),
            'password': forms.PasswordInput(attrs={
                            'class': 'form-control', 
                            'id': 'formGroupExampleInput',
                            'placeholder': 'Password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data

class UserSignupForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'confirm_password',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'username',
                'placeholder': 'Enter Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'Enter Email'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'password',
                'placeholder': 'Enter Password'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data

class ShopLoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class UploadFileForm(forms.Form):
    file = forms.FileField()

"""class UserUploadForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ['file', 'file_parent', 'price']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        files = self.files.getlist('file')
        if not files:
            raise forms.ValidationError("You must upload at least one file.")
        for file in files:
            if not file.name.endswith(('.pdf', '.doc', '.docx')):
                raise forms.ValidationError("Only PDF and DOC/DOCX files are allowed.")
        return cleaned_data"""