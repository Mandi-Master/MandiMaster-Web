from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields, ModelForm
from Home.models import Room, Topic,User


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email',"phoneNumber",'password1','password2']

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['avatar','username','email',"phoneNumber",'bio']


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['name']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ('__all__')
        exclude = ['host','participants']

    def __init__(self,*args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.fields['Type'].widget.attrs['class'] = 'form-control'
        self.fields['Category'].widget.attrs['class'] = 'form-control'
        self.fields['Title'].widget.attrs['class'] = 'form-control'
        self.fields['Price'].widget.attrs['class'] = 'form-control'
        self.fields['Currency'].widget.attrs['class'] = 'form-control'
        self.fields['Quantity'].widget.attrs['class'] = 'form-control'
        self.fields['City'].widget.attrs['class'] = 'form-control'
        self.fields['Address'].widget.attrs['class'] = 'form-control'
        self.fields['Description'].widget.attrs['class'] = 'form-control'
