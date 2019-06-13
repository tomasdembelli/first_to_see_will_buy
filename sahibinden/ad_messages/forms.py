from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MessageForm(forms.Form):
    text = forms.CharField(label='Message', max_length=200)
    #sender = forms.CharField(max_length=20)    # auto assign from the logged in user_name

'''
class FavouriteForm(forms.Form):
    is_favourite = forms.BooleanField(label='Favourite', required=False)
'''

class AdForm(ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description','price',]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email',]


'''
class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
'''


class SignUpForm(UserCreationForm):
    #first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    #last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    #email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    bio = forms.CharField(widget=forms.Textarea, max_length=500, required=False, help_text='Optional.')
    location = forms.CharField(max_length=30, help_text='Optional.', required=False,)


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'bio', 'location', 'birth_date', 'password1', 'password2', )    #username is from User model, email is just created, password1/s are from UserCreationForm    
        