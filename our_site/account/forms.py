from django import forms

class RealNameForm(forms.Form):
    realname = forms.CharField(label='Your real name', max_length=40)
    identity = forms.CharField(label='Your id card number', max_length=18)
    pic = forms.ImageField(label='Your face with your id card')

class CompositionForm(forms.Form):
    comp_name = forms.CharField(label='composition name', max_length=50)
    price = forms.DecimalField(label = 'price',max_digits=9, decimal_places=1)
    description = forms.CharField(label = 'description',max_length=500)
    text_field = forms.FileField(label = 'Text appendix',widget=forms.ClearableFileInput(attrs={'multiple': True}))
    picture_field = forms.FileField(label = 'Picture appendix',widget=forms.ClearableFileInput(attrs={'multiple': True}))
    video_field = forms.FileField(label = 'Video appendix',widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        abstract = True

class ProjectForm(CompositionForm):
    organization = forms.CharField(label = 'organization', max_length=25)
    start_time = forms.DateTimeField(label = 'start time')
    end_time = forms.DateTimeField(label = 'end time')