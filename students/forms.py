from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import Student

class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField()

    class Meta:
        model = Student
        fields = ['roll']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['username'].initial = user.username

    def save(self, commit=True):
        self.user.username = self.cleaned_data['username']
        self.user.save()
        return super().save(commit)


class PasswordChangeCustomForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Current password is incorrect.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")

        if new_password and self.user.check_password(new_password):
            raise forms.ValidationError("New password must be different from old password.")

        return cleaned_data
