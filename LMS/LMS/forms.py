from django.forms import ModelForm
from customuser.models import CustomUser


class signupForm(ModelForm):

    class Meta():
        model = CustomUser
        fields = '__all__'