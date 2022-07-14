from django.forms import ModelForm
from customuser.models import CustomUser
from django import forms
from django.contrib.auth.hashers import check_password
import re


class signupForm(ModelForm):

    class Meta():
        model = CustomUser
        fields = '__all__'

    # method for cleaning the data
    def clean(self):
        super(signupForm, self).clean()
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        phone_number = self.cleaned_data.get('phone_number')
        name = self.cleaned_data.get('name')

        if len(username) < 6:
            self._errors['username'] = self.error_class(
                ['Username must be at least 6 characters'])

        if len(password) < 8:
            self._errors['password'] = self.error_class(
                ['Password must be at least 8 characters'])

        if " " in username:
            self._errors['username'] = self.error_class(
                ['Username cannot contain white space'])

        if re.search(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+$", username):
            self._errors['username'] = self.error_class(
                ['Username contains invalid characters'])

        if re.search(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',
                     email) is None:
            self._errors['email'] = self.error_class(['Email is invalid'])

        if len(str(phone_number)) != 12:
            self._errors['phone number'] = self.error_class(
                ['Phone number must be 12 digits'])

        if re.search(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+$", name):
            self._errors['name'] = self.error_class(
                ['Name contains invalid characters'])

        if len(name) < 3:
            self._errors['name'] = self.error_class(
                ['Name must be at least 3 characters'])

        return self.cleaned_data
