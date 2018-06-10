from django import forms

class RealNameForm(forms.Form):
    realname = forms.CharField(label='Your real name', max_length=40)
    identity = forms.CharField(label='Your id card number', max_length=18)
    pic = forms.ImageField(label='Your face with your id card')
