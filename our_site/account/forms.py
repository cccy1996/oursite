from django import forms

class RealNameForm(forms.Form):
    realname = forms.CharField(label='Your real name', max_length=40)
    identity = forms.CharField(label='Your id card number', max_length=18)
    pic = forms.ImageField(label='Your face with your id card')

class CompositionForm(forms.Form):
    comp_name = forms.CharField(label='composition name', max_length=50)
    price = forms.DecimalField(label = 'price',max_digits=9, decimal_places=1)
    description = forms.CharField(label = 'description',max_length=500)
    appendixes = forms.FileField(label='Appendixes', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    pictures = forms.FileField(label='Pictures for display', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    videos = forms.FileField(label='Videos for display', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        abstract = True

class ProjectForm(CompositionForm):
    organization = forms.CharField(label = 'organization', max_length=25)
    start_time = forms.DateTimeField(label = 'start time')
    end_time = forms.DateTimeField(label = 'end time')

class PaperForm(CompositionForm):
    abstract = forms.CharField(label = 'abstract', max_length=200)
    keywords = forms.CharField(label = 'keywords', max_length=40)

class PatentForm(CompositionForm):
    patent_no = forms.CharField(label = 'patent number', max_length=15)
    apply_time = forms.DateTimeField(label = 'apply time')
    auth_time = forms.DateTimeField(label = 'authorized time')