import re

from django import forms
from django.core.exceptions import ValidationError

from mainapp.models import Student
from mainapp.widgets import ChangeImageSize


class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password', min_length=3, error_messages={'required':
         "Password can't be empty", 'min_length': "Password should have more than 3 characters"})
    logo_width = forms.IntegerField(required=False, widget=ChangeImageSize, label='Logo width')
    class Meta:
        model = Student
        fields = '__all__'
        error_message = {
            'name': {
                'required': "Username can't be empty",
                'max_length': 50
                }
            }
    def is_valid(self):
        print('validing',super().is_valid())
        return super().is_valid()

    def clean_password(self):   # function name: clean_ + field name
        # execute after previous validations are passed
        password = self.cleaned_data.get('password')
        print('p:',password)
        if all((re.search(r'\d+', password),re.search(r'[a-z]+', password), re.search(r'[A-Z]+', password))):
            print('valid key')
            return password
        else:
            print('p:x', password)
            raise ValidationError('Password need contain digit, upper case and lower case')