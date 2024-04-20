from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser



class CustomUserCreationForm(UserCreationForm):
    timezone = forms.CharField(required=False, initial='UTC')  # Значение по умолчанию 'UTC'

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'timezone']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.timezone = self.cleaned_data.get('timezone', 'UTC')
        if commit:
            user.save()
        return user


class NewUserPrivateDataForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'second_name', 'birth_day','age']


class UserProfilePictureForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['user_profile_pictures']


